# users/views.py

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from django.utils.timezone import now

# For email activation:
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

# Import your forms (make sure these exist in users/forms.py)
from users.forms import CustomRegisterForm, LoginForm, AssignRoleForm, CreateGroupForm

# Assuming you have an Event model in 'events' app
from events.models import Event # Make sure this import path is correct


# Test for users (remains the same)
def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def sign_up(request):
    form = CustomRegisterForm()

    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False  # Set user as inactive until activated
            user.save()

            # Assign 'User' group by default
            try:
                user_group = Group.objects.get(name='User')
                user.groups.add(user_group)
            except Group.DoesNotExist:
                messages.error(request, "Default 'User' group not found. Please create it in Django Admin.")
                # You might want to handle this more gracefully, e.g., create the group
                # or not assign if it doesn't exist.

            # --- Start: Send Activation Email ---
            current_site = get_current_site(request)
            mail_subject = 'Activate Your Event Management Account'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), # Encode user ID
                'token': default_token_generator.make_token(user), # Generate token
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            try:
                email.send()
                messages.success(request, "A confirmation email has been sent. Please check your inbox to activate your account.")
            except Exception as e:
                messages.error(request, f"Failed to send activation email. Please contact support. Error: {e}")
            # --- End: Send Activation Email ---

            return redirect('sign-in') # Redirect to sign-in page after sending email
    return render(request, 'registration/register.html', {"form": form})


def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Check if user is active before logging in
            if user.is_active:
                login(request, user)
                messages.success(request, f"Welcome, {user.username}!")
                return redirect('home') # Assuming 'home' is your main page
            else:
                messages.error(request, "Your account is not active. Please check your email for the activation link.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'registration/login.html', {'form': form})


@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect('sign-in')
    # Optional: Render a confirmation page for GET requests if you want to ask "Are you sure?"
    return redirect('home') # Or another appropriate page if GET is allowed


def activate_user(request, uidb64, token):
    try:
        # Decode the uidb64 to get the user's primary key
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None # User not found or invalid uid

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully! You can now log in.')
        return redirect('sign-in')
    else:
        messages.error(request, 'The activation link is invalid or has expired.')
        # You might want to render a specific template for failed activation
        return render(request, 'registration/activation_failed.html')


# --- Admin Dashboard and related views (assuming these are working correctly) ---

@user_passes_test(is_admin, login_url='no-permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')).all()
    events = Event.objects.select_related('category').prefetch_related('participants').all()
    groups = Group.objects.prefetch_related('permissions').all()
    today = now().date()
    todays_event = Event.objects.filter(date=today)

    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = 'No Group Assigned'

    context = {
        "users": users,
        'events': events,
        "todays_event": todays_event,
        'groups': groups,
    }
    return render(request, 'admin/dashboard.html', context)


@user_passes_test(is_admin, login_url='no-permission')
def assign_role(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('admin-dashboard')

    form = AssignRoleForm(instance=user) # Populate form if editing existing user roles

    if request.method == 'POST':
        form = AssignRoleForm(request.POST) # Form for POST data
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear() # Clear existing groups
            user.groups.add(role) # Add new role
            messages.success(request, f"User {user.username} has been assigned to the {role.name} role.")
            return redirect('admin-dashboard')

    return render(request, 'admin/assign_role.html', {"form": form, "user_to_assign": user})


@user_passes_test(is_admin, login_url='no-permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group '{group.name}' has been created successfully.")
            return redirect('group-list') # Redirect to group list after creation

    return render(request, 'admin/create_group.html', {'form': form})


@user_passes_test(is_admin, login_url='no-permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups': groups})


@user_passes_test(is_admin, login_url='no-permission')
def delete_user(request, user_id):
    if request.method == "POST":
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            messages.success(request, 'User deleted successfully.')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
        return redirect('admin-dashboard')
    else:
        messages.warning(request, 'Invalid request to delete user.') # Use warning for GET requests
        return redirect('admin-dashboard')


@user_passes_test(is_admin, login_url='no-permission')
def delete_group(request, grp_id):
    if request.method == "POST":
        try:
            group = Group.objects.get(id=grp_id)
            group.delete()
            messages.success(request, 'Group deleted successfully.')
        except Group.DoesNotExist:
            messages.error(request, 'Group not found.')
        return redirect('group-list')
    else:
        messages.warning(request, 'Invalid request to delete group.') # Use warning for GET requests
        return redirect('group-list')
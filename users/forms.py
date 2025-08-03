# from django import forms 
# import re
# from django.contrib.auth.models import User, Group, Permission
# from events.forms import StyledFormMixin
# from django.contrib.auth.forms import AuthenticationForm


# class CustomRegisterForm(StyledFormMixin, forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']


#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         email_exist = User.objects.filter(email=email).exists()

#         if email_exist:
#             raise forms.ValidationError('Email already exists')
#         return email

#     def clean_password(self):
#         password = self.cleaned_data.get("password")
#         errors = []

#         if len(password) < 8:
#             errors.append('Password must be at least 8 character long')

#         if not re.search(r'[A-Z]', password):
#             errors.append('Password must be at least one uppercase letter.')
        
#         if not re.search(r'[a-z]', password):
#             errors.append('Password must be at least one lowercase letter.')
        
#         if not re.search(r'[0-9]', password):
#             errors.append('Password must include at least one number.')
        
#         if not re.search(r'[@#$%^&+=]', password):
#             errors.append('Password must be at least one special character.')
        
#         if errors:
#             raise forms.ValidationError(errors)

#         return password
    
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')
            
#         if password and confirm_password and password != confirm_password:
#             raise forms.ValidationError("Password did not match")
        
#         return cleaned_data
        

# class LoginForm(StyledFormMixin, AuthenticationForm):
#     def __init__(self, *arg, **kwargs):
#         super().__init__(*arg, **kwargs)


# class AssignRoleForm(StyledFormMixin, forms.Form):
#     role = forms.ModelChoiceField(
#         queryset=Group.objects.all(),
#         empty_label="Select a Role"
#     )


# class CreateGroupForm(StyledFormMixin, forms.ModelForm):
#     permissions = forms.ModelMultipleChoiceField(
#         queryset=Permission.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False,
#         label='Assign Permission'
#     )

#     class Meta:
#         model = Group
#         fields = ['name', 'permissions']




# users/forms.py

from django import forms
import re
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.forms import AuthenticationForm
# Assuming 'StyledFormMixin' is defined in 'events.forms'
# If it's a generic mixin, it might be better placed in a common utils or base app.
from events.forms import StyledFormMixin


class CustomRegisterForm(StyledFormMixin, forms.ModelForm):
    # Use CharField with PasswordInput widget for password fields
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        # Ensure all fields are listed, and 'password', 'confirm_password' are handled by the form itself
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        # You can add widgets for other fields here if needed
        # widgets = {
        #     'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
        #     'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
        #     'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
        #     'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
        # }


    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Normalize email to handle case-insensitivity consistently
        email_norm = email.lower() if email else ''

        # Check for existing email. Use iexact for case-insensitive check.
        # Exclude the current user if this form were used for profile updates.
        # For registration, it's a straight check.
        if User.objects.filter(email__iexact=email_norm).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email_norm # Return normalized email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        errors = []

        if password: # Only validate if password is provided
            if len(password) < 8:
                errors.append('Password must be at least 8 characters long.')

            # Using lookaheads for more concise regex checks (optional, but cleaner)
            # (?=.*[A-Z])   - Must contain at least one uppercase letter
            # (?=.*[a-z])   - Must contain at least one lowercase letter
            # (?=.*[0-9])   - Must contain at least one digit
            # (?=.*[@#$%^&+=!]) - Must contain at least one special character from the set
            # Check for the overall structure rather than individual `re.search` calls for each rule
            if not re.fullmatch(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[@#$%^&+=!])(.{8,})$", password):
                if not re.search(r'[A-Z]', password):
                    errors.append('Password must contain at least one uppercase letter.')
                if not re.search(r'[a-z]', password):
                    errors.append('Password must contain at least one lowercase letter.')
                if not re.search(r'[0-9]', password):
                    errors.append('Password must include at least one number.')
                # Added '!' to the special characters set common for passwords
                if not re.search(r'[@#$%^&+=!]', password):
                    errors.append('Password must include at least one special character (e.g., @#$%^&+=!).')

        if errors:
            raise forms.ValidationError(errors)

        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Only compare if both passwords are provided and passed initial validation
        if password and confirm_password and password != confirm_password:
            # Add error specifically to confirm_password field for better UX
            self.add_error('confirm_password', "Passwords do not match.")
            # Or raise a non-field error if you prefer:
            # raise forms.ValidationError("Passwords do not match.")

        return cleaned_data


class LoginForm(StyledFormMixin, AuthenticationForm):
    # __init__ method is inherited from AuthenticationForm,
    # but you can override it if you want to add custom styling or attributes
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Example of adding a custom class for styling for username and password fields
        # self.fields['username'].widget.attrs.update({'class': 'my-custom-input-class'})
        # self.fields['password'].widget.attrs.update({'class': 'my-custom-input-class'})


class AssignRoleForm(StyledFormMixin, forms.Form):
    # Use ModelChoiceField for selecting a single Group object
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role",
        label="Assign Role" # Added a label for clarity
    )
    # If you intend to use this form to UPDATE an existing user's role,
    # you might want to pass the user instance to the form's __init__
    # and set initial data or limit queryset.
    # For example, in views.py (assign_role): form = AssignRoleForm(initial={'role': user.groups.first()})


class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    # ModelMultipleChoiceField for selecting multiple Permission objects
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False, # Permissions are optional when creating a group
        label='Assign Permissions' # Plural for clarity
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']
        # You can add widgets here for the 'name' field if needed
        # widgets = {
        #     'name': forms.TextInput(attrs={'placeholder': 'Enter group name'})
        # }
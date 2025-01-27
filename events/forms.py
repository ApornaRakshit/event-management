from django import forms
from events.models import Event


class EventForm(forms.Form):
    title = forms.CharField(max_length=250, label="Event Title")
    description = forms.CharField(
        widget=forms.Textarea, label='Event Description')
    due_date = forms.DateField(widget=forms.SelectDateWidget, label="Due Date")
    assigned_to = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=[], label="Assigned To")

    def __init__(self, *args, **kwargs):
        # print(args,kwargs)
        employees= kwargs.pop("employees",[])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices=[
            (emp.id, emp.name) for emp in employees]
        
# class StyledFormMinin:
#     """ Mixing to apply to form field"""

#     default_classes = "border-2 border-gray-500 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-400 focus:ring-rose-500"
    
#     def apply_styled_widgets(self):
#        for field_name, field in self.fields.items():
#            if isinstance(field.widget, forms.TextInput):
#                field.widget.attrs.update({
#                    'class':self.default_classes,
#                    'placeholder':f"Enter {field.label.lower()}"
#                })
#            elif isinstance(field.widget, forms.Textarea):
#                field.widget.attrs.update({
#                    'class':self.default_classes,
#                    'placeholder':f"Enter {field.label.lower()}",
#                    'rows': 5
#                })
#            elif isinstance(field.widget, forms.SelectDateWidget):
#                field.widget.attrs.update({
#                    'class':self.default_classes,
#                })
#            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
#                field.widget.attrs.update({
#                    'class':"space-y-2",
#                })


class StyledFormMixin:
    """ Mixing to apply style to form field"""

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()

    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                # print("Inside Date")
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                # print("Inside checkbox")
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            # else:
            #     # print("Inside else")
            #     field.widget.attrs.update({
            #         'class': self.default_classes
            #     })


class EventModelForm(StyledFormMixin, forms.ModelForm):  
    class Meta:
        model = Event
        fields = ['title','description','due_date', 'assigned_to']
        widgets = {
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple
        }


        # exclude = ['project', 'is_completed', 'created_at', 'updated_at']   
        """ Manual Widgets """
        # widgets = {
        #     'title': forms.TextInput(attrs={
        #         'class': "border-2 border-gray-500 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-400 focus:ring-rose-500",
        #         "placeholder":"Enter class title"
        #     }),
        #     'description': forms.Textarea(attrs={
        #         'class': "border-2 border-gray-500 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-400 focus:ring-rose-500",
        #         "placeholder":"Enter class description"
        #     }),
        #     'due_date': forms.SelectDateWidget(attrs={
        #         'class': "border-2 border-gray-300 p-2 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500",
        #     }),
        #     'assigned_to': forms.CheckboxSelectMultiple(attrs={
        #         'class': "space-y-2",
        #     })
        # }  

        def __init__(self, *arg, **kwarg):
            super().__init__(*arg, **kwarg)
            self.apply_styled_widgets()
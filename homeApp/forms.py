from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-group'
        self.fields['password1'].widget.attrs['class'] = 'form-group'
        self.fields['password2'].widget.attrs['class'] = 'form-group'
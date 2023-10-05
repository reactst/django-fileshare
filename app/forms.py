from django import forms
from .models import User, Documents

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=User.roles, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'role']



class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ['title', 'doc']

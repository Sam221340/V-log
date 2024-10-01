from django import forms


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='Username',max_length=20,widget=forms.TextInput)
    email = forms.EmailField(label='Your email',max_length=30)
    password = forms.CharField(label='Enter password',max_length=10)
    confirm_password = forms.CharField(label='Confirm password',max_length=10,widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(label='Username',max_length=20,widget=forms.TextInput)
    password = forms.CharField(label='Enter password',max_length=10)

# forms.py
class Reset_Password(forms.Form):
    email = forms.EmailField(label='Your email')
    new_password = forms.CharField(label="New password",max_length=16)
    Confirm_password = forms.CharField(label='Confirm password',widget=forms.PasswordInput)

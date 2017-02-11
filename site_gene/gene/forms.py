from django.contrib.auth import authenticate
import django.db
from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    email = forms.EmailField(label='email')
    password1 = forms.CharField(label='password1', max_length=100, widget=forms.widgets.PasswordInput())
    password2 = forms.CharField(label='password2', max_length=100)

    def clean(self):

        if not self.captcha:
            raise forms.ValidationError('captcha failed')

        cleaned_data = super(RegisterForm, self).clean()
        
        pw1 = cleaned_data.get('password1')
        pw2 = cleaned_data.get('password2')

        if pw1 != pw2:
            raise forms.ValidationError("Passwords do not match")


        try:
            user = User.objects.create_user(
                    cleaned_data['username'],
                    cleaned_data['email'],
                    cleaned_data['password1'])
        except django.db.IntegrityError as e:
            raise forms.ValidationError("Username already taken")
        
        user.is_active = False

        user.save()
        


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', max_length=100, widget=forms.widgets.PasswordInput())
       
    def clean(self):
 
        if not self.captcha:
            raise forms.ValidationError('captcha failed')
       
        cleaned_data = super(LoginForm, self).clean()
        
        self.user_cache = authenticate(
                username=cleaned_data['username'],
                password=cleaned_data['password'])

        if self.user_cache is None:
            raise forms.ValidationError("Invalid username or password")

        if not self.user_cache.is_active:
            raise forms.ValidationError("User is inactive")


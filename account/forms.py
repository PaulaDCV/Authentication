from django import forms
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField
from account.models import Account
from django.contrib.auth import authenticate

class RegistrationForm(UserCreationForm):
    customer_email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address.')

    class Meta:
        model = Account
        fields = ('customer_email', 'username', "date_birth", "address", 'password1', 'password2')


class AuthenticateUsersForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("customer_email", "password")

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['customer_email']
            password = self.cleaned_data['password']
            if not authenticate(customer_email=email, password=password):
                raise forms.ValidationError("Invalid login")


class ReCAPTCHAForm(forms.Form):
    captcha = ReCaptchaField()

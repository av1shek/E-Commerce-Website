from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignupForm(forms.Form):
    email = forms.EmailField(max_length=200, help_text='Required')
    username = forms.RegexField(regex="^[\w.@+-]+\Z", error_messages={'invalid': 'Enter Proper Username'})
    password1 = forms.CharField(widget=forms.PasswordInput(), validators=[
                                RegexValidator('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).{8,}$')], error_messages={'invalid': "Enter valid password"})
    password2 = forms.CharField(widget=forms.PasswordInput(),)
    fname = forms.CharField(max_length=90, help_text='Required')
    lname = forms.CharField(max_length=90)
    mobno = forms.CharField(max_length=90, help_text='Required')
    address = forms.CharField(max_length=200)
    city = forms.CharField(max_length=50)
    zip_code = forms.CharField(max_length=50)
    state = forms.CharField(max_length=50)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = None
        try:
            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist as e:
                pass
            except Exception as e:
                raise e
            if not user:
                pass
            elif not user.is_active:
                pass
            else:
                raise forms.ValidationError("This Username Already Exists")
        except Exception as e:
            raise e
        return username


    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = None
        try:
            try:
                user = User.objects.get(email=email)
            except ObjectDoesNotExist as e:
                pass
            except Exception as e:
                raise e
            if not user:
                pass
            elif not user.is_active:
                pass
            else:
                raise forms.ValidationError(
                    "User with this email ID Already Exists")
        except Exception as e:
            raise forms.ValidationError(
                "User with this email ID Already exists")
        return email

    def clean_password2(self):
        print("executing clean_password")
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Passwords doesn't Match")
        return password2


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'name', 'fname', 'lname', 'mobno', 'address', 'city', 'zip_code', 'state')
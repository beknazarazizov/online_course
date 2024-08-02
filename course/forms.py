from django.contrib.auth.forms import UserModel
from django.contrib.auth.models import User
from django import forms

from course.models import Course, Comment
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()




    def clean_email(self):
        email = self.data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email does not exist')
        return email

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.data.get('password')
        try:
            user = User.objects.get(email=email)
            print(user)
            if not user.check_password(password):
                raise forms.ValidationError('Password did not match')
        except User.DoesNotExist:
            raise forms.ValidationError(f'{email} does not exists')
        return password

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(max_length=128)
    password2 = forms.CharField(max_length=128)

    class Meta:
        model = UserModel
        fields = ['username', 'email',]

class UserModelForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        exclude=()

class EmailForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    email_from = forms.EmailField()
    email_to = forms.EmailField()

class CommentModelForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment']
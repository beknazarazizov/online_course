import random
from random import random

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from email.message import EmailMessage

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import FormView

from config.settings import EMAIL_HOST_USER
from course.models import UserConfirmationModel
from course.token import account_activation_token


from course.forms import LoginForm, EmailForm, RegistrationForm
from django.views.generic.edit import CreateView


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'registration/login_page.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user =User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been activated successfully!😊')
        return redirect('customers')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('register')


def activate_email(request, user, to_email):
    subject = 'Activate your account'
    message = render_to_string('registration/template_activate_accaunt.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'protocol': 'https' if request.is_secure() else 'http',
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(subject, message, to=[to_email])
    try:
        email.send()
        messages.success(request,
                         'Activation email has been sent. You have 5 minut to activate your account. '
                         'Please check your email')
    except Exception as e:
        messages.error(request, f'Sorry, there was an error sending the activation email: {str(e)}')


def send_confirmation_email(email):
    subject = 'Confirm Your Email'
    code = random.randint(1000, 9999)
    if UserConfirmationModel.objects.filter(code=code).exists():
        send_confirmation_email(email)
    emails = [email]
    from_email = EMAIL_HOST_USER
    if send_mail(subject=subject, message=str(code), from_email=from_email, recipient_list=emails):
        UserConfirmationModel.objects.create(
            code=code,
            email=email,
            is_active=True,
        )
        return True
    else:
        return False


class RegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('confirm')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.is_active = False
        user.save()
        email = form.cleaned_data['email']
        if send_confirmation_email(email=email):
            return super().form_valid(form)
        else:
            return redirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class LoginPageView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'registration/login_page.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid username or password.')
        return render(request, 'registration/login_page.html', {'form': form})


def logout_page(request):
    if request.method == 'GET   ':
        logout(request)
        return redirect('register')
    return render(request,'registration/register.html')


class SendEmailView(View):
    def get(self, request):
        form = EmailForm()
        context = {'form': form}
        return render(request, 'email/send_email.html', context)

    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email_from = form.cleaned_data['email_from']
            email_to = [form.cleaned_data['email_to']]
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, email_from, email_to)
                messages.success(request, 'Message sent successfully.')
                return redirect('customers')
            except Exception as e:
                messages.error(request, f'Error sending message: {e}')

        context = {'form': form}
        return render(request, 'email/send_email.html', context)


def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print('-------------------------------')
        print(user)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your email has been verified.')
        return redirect('customers')
    else:
        messages.warning(request, 'The link is invalid.')

    return render(request, 'email/verify_email_confirm.html')


def verify_email_done(request):
    return render(request, 'email/verify_email_done.html')


def confirmation_view(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        user_code = UserConfirmationModel.objects.get(code=code)
        if user_code:
            user = User.objects.get(email=user_code.email)
            user.is_active = True
            user.save()
            return redirect('login')
        else:
            return redirect('home')
    else:
        return render(request, 'registration/confirmation.html')



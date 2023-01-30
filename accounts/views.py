from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import LoginForm, RegisterForm, EditAccountForm, EditSuperAccountForm
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .models import User
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site


def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']

                user_auth = auth.authenticate(email=email, password=password)

                if user_auth is not None:
                    auth.login(request, user=user_auth)
                    messages.success(request, 'You are now logged in')

                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    else:
                        return redirect('dashboard')

                else:
                    messages.error(request, 'Given user is not exists')
                    if 'next' in request.POST:
                        return redirect(f"?next={request.POST.get('next')}")

            else:
                if form.errors:
                    for field in form:
                        for error in field.errors:
                            messages.error(request, f"{error}")

        else:
            form = LoginForm

        return render(request, 'accounts/login.html', {'form': form})


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('dashboard')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = request.POST['password']

            user = User.objects.create_user(
                first_name=first_name, last_name=last_name, username=username, email=email, password=password
            )

            user.role = 2
            user.phone_number = phone_number
            user.is_active = True

            user.save()

            messages.success(request, 'Your account has been successfully registered! You should now login')
            return redirect('dashboard')
        else:
            if form.errors:
                for field in form:
                    for error in field.errors:
                        messages.error(request, f"{error}")

    else:
        form = RegisterForm

    return render(request, 'accounts/register.html', {'form': form})


@login_required(login_url='login')
def edit_account(request):
    if request.user.is_superuser:
        user = User.objects.get(id=request.user.id)
        if request.method == 'POST':
            form = EditSuperAccountForm(data=request.POST, instance=user)
            if form.is_valid():
                messages.success(request, 'You have successfully edited your superuser account!')
                form.save()
                return redirect('dashboard')
            else:
                if form.errors:
                    for field in form:
                        for error in field.errors:
                            messages.error(request, f"{error}")
        else:
            form = EditSuperAccountForm(instance=user)

        return render(request, 'accounts/edit_account.html', {'form': form})
    else:
        user = User.objects.get(id=request.user.id)
        if request.method == 'POST':
            form = EditAccountForm(data=request.POST, instance=user)
            if form.is_valid():
                messages.success(request, 'You have successfully edited your account!')
                form.save()
                return redirect('dashboard')
            else:
                if form.errors:
                    for field in form:
                        for error in field.errors:
                            messages.error(request, f"{error}")
        else:
            form = EditAccountForm(instance=user)

        return render(request, 'accounts/edit_account.html', {'form': form})


def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            mail_subject = 'Change your password'
            template_name = 'accounts/change_password_validate.html'
            message = render_to_string(template_name, {
                'user': user,
                'domain': get_current_site(request),
                'uid': urlsafe_base64_encode(force_bytes(user.id)),  # it will encode your id
                'token': default_token_generator.make_token(user),
            })
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = user.email
            mail = EmailMessage(mail_subject, message, from_email, [to_email])
            mail.content_subtype = "html"
            mail.send()
            messages.success(request, 'We sent you an link to your email to change password.')
            return redirect('login')

    return render(request, 'accounts/forget_password.html')


def change_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(ValueError, TypeError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please change your password.')
        return redirect('change_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('dashboard')


def change_password(request):
    if request.session.get('uid'):
        if request.method == 'POST':
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            if password == confirm_password:
                pk = request.session.get('uid')
                user = User.objects.get(pk=pk)
                user.set_password(password)
                user.save()
                del request.session['uid']
                messages.success(request, 'You have now new password set!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Password does not match!')
                return redirect('change_password')

        return render(request, 'accounts/change_password.html')
    else:
        return redirect('dashboard')

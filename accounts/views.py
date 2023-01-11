from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from django.contrib import auth
from .models import User


def login(request):
    if request.user.is_authenticated and request.user.is_active:
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
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Given user is not exist')
                    return redirect('login')
            else:
                if form.errors:
                    for field in form:
                        for error in field.errors:
                            messages.error(request, f"{error}")

        else:
            form = LoginForm

        return render(request, 'accounts/login.html', {'form': form})


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

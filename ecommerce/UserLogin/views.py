from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from .forms import RegisterForm, LoginForm
from django.utils.http import url_has_allowed_host_and_scheme as is_safe_url
from django.contrib import messages

User = get_user_model()


def register_page(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        new_user = User.objects.create_user(
            email, password, first_name, last_name)
        if new_user is not None:
            messages.success(request, "Created User.")
            return redirect('UserLogin:login')

        messages.warning(request, "Create Error !")

    context = {
        "form": form
    }

    return render(request, "UserLogin/register.html", context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('homepage')

    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            request.session['customer'] = user.email
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('homepage')
        else:
            messages.warning(request, 'Credentials error.')

    return render(request, "UserLogin/login.html", context)

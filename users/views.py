from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import auth
from .forms import RegistrationForm, LoginForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']

            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password, email=email)

            user_profile = UserProfile(user=user)
            user_profile.save()

            return HttpResponseRedirect("/login/")

    else:
        form = RegistrationForm()

    return render(request, 'users/registration.html', {'form':form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('users:profile', args=[user.id]))
            else:
                return render(request, 'user/login.html', {'form':form, 'message': 'Wrong password. Please try again.'})

    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

def profile(request):
    return HttpResponse("Welcome")

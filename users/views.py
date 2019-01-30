from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile, Ride
from django.contrib import auth
from .forms import RegistrationForm, LoginForm, DriverForm, RideForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('users:homepage'))

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

            return HttpResponseRedirect("/users/login/")

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
                return render(request, 'users/login.html', {'form':form, 'message': 'Wrong password. Please try again.'})

    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

@login_required
def profile(request, id):
    user = get_object_or_404(User, id=id)
    user_profile = get_object_or_404(UserProfile, user=user)
    
    return render(request, 'users/profile.html', {'user': user, 'user_profile':user_profile})

@login_required
def regisdriver(request, id):
    user = get_object_or_404(User, id=id)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        form = DriverForm(request.POST)

        if form.is_valid():
            # driver update
            user_profile.driver = True
            user_profile.vehicle = form.cleaned_data['vehicle']
            user_profile.plate = form.cleaned_data['plate']
            user_profile.capacity = form.cleaned_data['capacity']
            user_profile.special = form.cleaned_data['special']
            user_profile.save()

            return HttpResponseRedirect(reverse('users:profile', args=[user.id]))

    else:
        form = DriverForm()

    return render(request, 'users/regisdriver.html', {'form': form, 'user': user})

@login_required
def display(request, id):
    user = get_object_or_404(User, id=id)
    user_profile = get_object_or_404(UserProfile, user=user)
    
    return render(request, 'users/display.html', {'user': user, 'user_profile': user_profile})

def homepage(request):
    return render(request, 'users/homepage.html')

@login_required
def newride(request, id):
    user = get_object_or_404(User, id=id)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        form = RideForm(request.POST)

        if form.is_valid():
            # status default open
            destination = form.cleaned_data['destination']
            arrivaldate = form.cleaned_data['arrivaldate']
            passenger = form.cleaned_data['passenger']
            sharable = form.cleaned_data['sharable']
            vehicle = form.cleaned_data['vehicle']
            special = form.cleaned_data['special']
            rider_id = id

            ride = Ride(destination=destination, arrivaldate=arrivaldate, passenger=passenger, sharable=sharable, vehicle=vehicle, special=special, rider_id=rider_id)
            ride.save()

            return HttpResponseRedirect(reverse('users:curtride', args=[user.id, ride.id]))
    else:
        form = RideForm()
    return render(request, 'users/newride.html', {'form': form, 'user': user})

@login_required
def curtride(request, id, rid):
    return HttpResponse("Hi There")

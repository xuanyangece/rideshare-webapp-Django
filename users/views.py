from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile, Ride
from django.contrib import auth
from .forms import RegistrationForm, LoginForm, DriverForm, RideForm, RideEditForm, ShareForm, PasswordForm, ShareEditForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.mail import send_mail


# homepage before login
def homepage(request):
    return render(request, 'users/homepage.html')

# logout your account
@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('users:homepage'))

# register a new account
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

# login into your account
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

# profile info page
@login_required
def profile(request, id):
    user = get_object_or_404(User, id=id)
    user_profile = get_object_or_404(UserProfile, user=user)
    
    return render(request, 'users/profile.html', {'user': user, 'user_profile':user_profile})

# register as a driver
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

# main user page, display rides info
@login_required
def display(request, id):
    user = get_object_or_404(User, id=id)
    user_profile = get_object_or_404(UserProfile, user=user)

    # rider
    # open rides
    queryset1 = Ride.objects.filter(status='open', rider_id=id)
    openrides_temp = list(queryset1)
    openrides = []
    for one in openrides_temp:
        temp_sharers = []
        for i in range(0, len(one.sharer_id)):
            curt_sharer = get_object_or_404(User, id=one.sharer_id[i]).first_name
            curt_psg = one.sharer_passenger[i]
            temp_sharers.append({'name': curt_sharer, 'num': curt_psg})
        openrides.append({'destination': one.destination, 'arrivaldate': one.arrivaldate, 'sharers': temp_sharers, 'id': one.id, 'group': len(one.sharer_id)})

    # confirmed rides
    queryset2 = Ride.objects.filter(status='confirmed', rider_id=id)
    confirmedrides = list(queryset2)
    cfm_info_rider = []
    for i in range(0, len(confirmedrides)):
        # get driver info
        curt_driver_id = confirmedrides[i].driver_id
        curt_driver = get_object_or_404(User, id=curt_driver_id)
        driver_name = curt_driver.first_name
        vehicle_info = get_object_or_404(UserProfile, user=curt_driver).vehicle
        curt_destination = confirmedrides[i].destination
        curt_arrivaldate = confirmedrides[i].arrivaldate
        # get sharer info
        temp_sharers = []
        for j in range(0, len(confirmedrides[i].sharer_id)):
            curt_sharer = get_object_or_404(User, id=confirmedrides[i].sharer_id[j]).first_name
            curt_psg = confirmedrides[i].sharer_passenger[j]
            temp_sharers.append({'name': curt_sharer, 'num': curt_psg})
        cfm_info_rider.append({'destination': curt_destination, 'arrivaldate': curt_arrivaldate, 'driver_name': driver_name, 'vehicle_info': vehicle_info, 'sharers': temp_sharers, 'id': confirmedrides[i].id, 'group': len(confirmedrides[i].sharer_id)})

    # driver
    queryset3 = Ride.objects.filter(~Q(status='complete'), driver_id=id)
    drive = list(queryset3)
    # if has current drive
    has_drive = len(drive) > 0
    owner = ''
    sharers = []
    if has_drive:
        drive = drive[0]
        owner = get_object_or_404(User, id=drive.rider_id).first_name
        for i in range(0, len(drive.sharer_id)):
            curt_share_id = drive.sharer_id[i]
            name = get_object_or_404(User, id=curt_share_id).first_name
            num_psg = drive.sharer_passenger[i]
            curt_sharer = {'name': name, 'num': num_psg}
            sharers.append(curt_sharer)

    # share
    # unconfirmed
    queryset4 = Ride.objects.filter(status='open')
    tempopenshare = list(queryset4)
    openshares = []
    for one in tempopenshare:
        if id in one.sharer_id:
            openshares.append(one)

    # confirmed
    queryset5 = Ride.objects.filter(status='confirmed')
    tempconfirmedshare = list(queryset5)
    confirmedshares = []
    for one in tempconfirmedshare:
        if id in one.sharer_id:
            curt_rider_id = one.rider_id
            rider_name = get_object_or_404(User, id=curt_rider_id).first_name
            curt_driver_id = one.driver_id
            curt_driver = get_object_or_404(User, id=curt_driver_id)
            driver_name = curt_driver.first_name
            vehicle_info = get_object_or_404(UserProfile, user=curt_driver).vehicle
            confirmedshares.append({'rider_name': rider_name, 'destination': one.destination, 'arrivaldate': one.arrivaldate, 'driver_name': driver_name, 'vehicle_info': vehicle_info})

    context = {
        'user': user,
        'user_profile': user_profile,
        'has_drive': has_drive,
        'drive': drive,
        'openrides': openrides,
        'cfm_info_rider': cfm_info_rider,
        'openshares': openshares,
        'confirmedshares': confirmedshares,
        'owner': owner,
        'sharers': sharers
    }
    return render(request, 'users/display.html', context)

# start a new ride as rider
@login_required
def newride(request, id):
    user = get_object_or_404(User, id=id)

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

            return HttpResponseRedirect(reverse('users:display', args=[id]))
    else:
        form = RideForm()
    return render(request, 'users/newride.html', {'form': form, 'user': user})

# edit current ride for rider
@login_required
def curtride(request, id, rid):
    user = get_object_or_404(User, id=id)
    user_profile = get_object_or_404(UserProfile, user=user)
    ride = get_object_or_404(Ride, id=rid)

    # prevent race
    if ride.status == 'open':
        if request.method == 'POST':
            form = RideEditForm(request.POST)
            if form.is_valid():
                # status default open
                ride.destination = form.cleaned_data['destination']
                ride.arrivaldate = form.cleaned_data['arrivaldate']
                ride.passenger = form.cleaned_data['passenger']
                ride.vehicle = form.cleaned_data['vehicle']
                ride.special = form.cleaned_data['special']

                ride.save()
                return HttpResponseRedirect(reverse('users:display', args=[user.id]))
        else:
            defaultData = {
                'destination': ride.destination,
                'arrivaldate': ride.arrivaldate,
                'passenger': ride.passenger,
                'vehicle': ride.vehicle,
                'special': ride.special
            }
            form = RideEditForm(defaultData)
        return render(request, 'users/curtride.html', {'user': user, 'user_profile': user_profile, 'form': form})
    else:
        return HttpResponseRedirect(reverse('users:display', args=[id]))

# driver clicked confirmed
@login_required
def complete(request, id, rid):
    ride = get_object_or_404(Ride, id=rid)
    if ride.status is not 'complete':
        ride.status = 'complete'
        ride.save()

    # send emails

    return HttpResponseRedirect(reverse('users:display', args=[id]))

# find available rides for driver
@login_required
def findridedriver(request, id):
    user = get_object_or_404(User, id=id)
    user_profile = get_object_or_404(UserProfile, user=user)

    # access all available open rides for driver
    queryset = Ride.objects.filter(Q(vehicle=user_profile.vehicle) | Q(vehicle=''), Q(special='') | Q(special=user_profile.special), ~Q(rider_id=id), status='open')
    temp = list(queryset)
    rides = []
    # condition for passenger limit&sharer
    for ride in temp:
        # continue if driver's sharer
        if ride in ride.sharer_id:
            continue
        totalpsg = ride.passenger
        # add sharer
        for number in ride.sharer_passenger:
            totalpsg += number
        if totalpsg <= user_profile.capacity:
            rides.append(ride)
        ride.total_psg = totalpsg

    return render(request, 'users/findridedriver.html', {'user': user, 'user_profile': user_profile, 'rides': rides})

# for confirmation
@login_required
def handledrive(request, id, rid):
    ride = get_object_or_404(Ride, id=rid)
    # prevent race 
    if ride.status == 'open':
        ride.status = 'confirmed'
        ride.driver_id = id
        ride.save()
        
        # send email to rider & sharers
        receivers = []
        rider_email = get_object_or_404(User, id=ride.rider_id).email
        receivers.append(rider_email)
        for sid in ride.sharer_id:
            sharer_email = get_object_or_404(User, id=sid).email
            receivers.append(sharer_email)
        send_mail(
            'Drive Comfirmed!',
            'Your drive to ' + ride.destination + ' is confirmed!',
            'ridesharexy@hushmail.com',
            receivers,
            fail_silently=False,
        )


    return HttpResponseRedirect(reverse('users:display', args=[id]))

# delete ride if not confirmed
@login_required
def delete(request, id, rid):
    ride = get_object_or_404(Ride, id=rid)
    # prevent race
    if ride.status == 'open':
        ride.delete()
    return HttpResponseRedirect(reverse('users:display', args=[id]))

# fill info to look up new ride as share
@login_required
def newshare(request, id):
    user = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        form = ShareForm(request.POST)

        if form.is_valid():
            destination = form.cleaned_data['destination']
            passenger = form.cleaned_data['passenger']
            earlyarrival = form.cleaned_data['earlyarrival']
            latearrival = form.cleaned_data['latearrival']

            queryset = Ride.objects.filter(~Q(driver_id=id), ~Q(rider_id=id), status='open', destination=destination, arrivaldate__range=[earlyarrival, latearrival])
            # not include sharer itself
            sharerides = []
            temp = list(queryset)
            for one in temp:
                if id not in one.sharer_id:
                    sharerides.append(one)

            return render(request, 'users/shareresult.html', {'user': user, 'sharerides': sharerides, 'passenger': passenger})
    else:
        form = ShareForm()
    return render(request, 'users/newshare.html', {'form': form, 'user': user})

# handle ride for new join sharer
@login_required
def joinshare(request, id, rid, passenger):
    ride = get_object_or_404(Ride, id=rid)
    # prevent race
    if ride.status == 'open':
        ride.sharer_id.append(id)
        ride.sharer_passenger.append(passenger)
        ride.save()

    return HttpResponseRedirect(reverse('users:display', args=[id]))

# handle delete share
@login_required
def deleteshare(request, id, rid):
    ride = get_object_or_404(Ride, id=rid)
    # prevent race
    if ride.status == 'open':
        # find sharer index
        index = ride.sharer_id.index(id)
        ride.sharer_id.remove(id)
        # delete in sharer_passenger
        del ride.sharer_passenger[index]
        ride.save()

    return HttpResponseRedirect(reverse('users:display', args=[id]))

# edit driver info
def editinfo(request, id):
    user = get_object_or_404(User, id=id)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        form = DriverForm(request.POST)

        if form.is_valid():
            user_profile.vehicle = form.cleaned_data['vehicle']
            user_profile.plate = form.cleaned_data['plate']
            user_profile.capacity = form.cleaned_data['capacity']
            user_profile.special = form.cleaned_data['special']
            user_profile.save()

            return HttpResponseRedirect(reverse('users:profile', args=[user.id]))
    else:
        defaultData = {
            'vehicle': user_profile.vehicle,
            'plate': user_profile.plate,
            'capacity': user_profile.capacity,
            'special': user_profile.special,
        }
        form = DriverForm(defaultData)

        return render(request, 'users/editinfo.html', {'user': user, 'user_profile': user_profile, 'form': form})

# change password
@login_required
def changepassword(request, id):
    user = get_object_or_404(User, id=id)
    # if we have to update user_profile?

    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['oldpassword']
            username = user.username

            curt_user = auth.authenticate(username=username, password=password)

            if curt_user is not None and curt_user.is_active:
                new_password = form.cleaned_data['password2']
                curt_user.set_password(new_password)
                curt_user.save()
                
                return HttpResponseRedirect(reverse('users:login'))
            else:
                return render(request, 'users/changepassword.html', {'user': user, 'form': form, 'message': 'Old password is wrong. Try again.'})

        # when form is not valid
        form = PasswordForm()

        return render(request, 'users/changepassword.html', {'user': user, 'form': form, 'message': 'Password format not correct, try again.'})
    else:
        form = PasswordForm()
        
        return render(request, 'users/changepassword.html', {'user': user, 'form': form})

# sharer edit passenger
@login_required
def editshare(request, id, rid):
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = ShareEditForm(request.POST)
        if form.is_valid():
            passenger = form.cleaned_data['passenger']
            ride = get_object_or_404(Ride, id=rid)
            index = ride.sharer_id.index(id)
            ride.sharer_passenger[index] = passenger
            ride.save()

            return HttpResponseRedirect(reverse('users:display', args=[user.id]))
    else:
        form = ShareEditForm()

        return render(request, 'users/editshare.html', {'form': form, 'user': user})

from django import forms
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
import re

def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)

class RegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=40)
    first_name = forms.CharField(label='Firstname', max_length=30)
    last_name = forms.CharField(label='Lastname', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    # set rules for validation

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if len(username) < 6:
            raise forms.ValidationError("Your username must be at least 6 characters.")
        elif len(username) > 40:
            raise forms.ValidationError("Your username should be less than 41 characters.")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError("Your username already exists.")
        
        return username

    def clean_name(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')

        if len(first_name) > 30:
            raise forms.ValidationError("Your first name should be less than 31 characters.")
        elif len(last_name) > 30:
            raise forms.ValidationError("Your last name should be less than 31 characters.")
        
        return first_name

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email_check(email):
            filter_result = User.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("Your email already exists.")
        else:
            raise forms.ValidationError("Please enter a valid email.")

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 8:
            raise forms.ValidationError("Password should be at least 8 characters.")
        elif len(password1) > 20:
            raise forms.ValidationError("Password cannot exceed 20 characters.")
        
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password mismatch. Please enter again.")

        return password2

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=40)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    # set rules for validation

    def clean_username(self):
        username = self.cleaned_data.get('username')
        filter_result = User.objects.filter(username__exact=username)
        if not filter_result:
            raise forms.ValidationError("This username does not exist.")
        
        return username

class DriverForm(forms.Form):
    # driver firld hidden
    vehicle = forms.CharField(label='Vehicle Type', max_length=20)
    plate = forms.CharField(label='License Plate Number', max_length=10)
    capacity = forms.IntegerField(label='Passenger Capacity', validators=[MaxValueValidator(200),MinValueValidator(1)])
    special = forms.CharField(label='Special Info', max_length=200, widget=forms.Textarea, help_text=' (optional)', required=False)

    # set rule for validation

    def clean_vehicle(self):
        vehicle = self.cleaned_data.get('vehicle')

        if len(vehicle) == 0:
            raise forms.ValidationError("Your vehicle type cannot be empty.")
        elif len(vehicle) > 20:
            raise forms.ValidationError("Your vehicle type cannot exceed 20 characters.")

        return vehicle
    
    def clean_plate(self):
        plate = self.cleaned_data.get('plate')

        if len(plate) == 0:
            raise forms.ValidationError("Your plate number cannot be empty.")
        elif len(plate) > 10:
            raise forms.ValidationError("Your plate number cannot exceed 10 characters.")
        
        return plate
    
    def clean_special(self):
        special = self.cleaned_data.get('special')

        if len(special) > 200:
            raise forms.ValidationError("Special info cannot exceed 200 characters.")

        return special

class RideForm(forms.Form):
    destination = forms.CharField(label='Destination', max_length=50)
    arrivaldate = forms.DateTimeField(label='Required Arrival Date&Time', help_text=' format: 2006-10-25 14:30')
    passenger = forms.IntegerField(label='Number of Passengers', validators=[MaxValueValidator(200),MinValueValidator(1)])
    sharable = forms.BooleanField(label='Willing to share this ride? (cannot change once submit)', required=False)
    vehicle = forms.CharField(label='Vehicle Type', max_length=20, help_text=' (optional)', required=False)
    special = forms.CharField(label='Special Request', max_length=200, widget=forms.Textarea, help_text=' (optional)', required=False)

class RideEditForm(forms.Form):
    destination = forms.CharField(label='Destination', max_length=50)
    arrivaldate = forms.DateTimeField(label='Required Arrival Date&Time', help_text=' format: 2006-10-25 14:30')
    passenger = forms.IntegerField(label='Number of Passengers', validators=[MaxValueValidator(200),MinValueValidator(1)])
    vehicle = forms.CharField(label='Vehicle Type', max_length=20, help_text=' (optional)', required=False)
    special = forms.CharField(label='Special Request', max_length=200, widget=forms.Textarea, help_text=' (optional)', required=False)

class ShareForm(forms.Form):
    destination = forms.CharField(label='Destination', max_length=50)
    passenger = forms.IntegerField(label='Number of Passengers', validators=[MaxValueValidator(200),MinValueValidator(1)])
    earlyarrival = forms.DateTimeField(label='Earliest Arrival Expected', help_text=' format: 2019-10-25 14:30')
    latearrival = forms.DateTimeField(label='Latest Arrival Expected', help_text=' format: 2019-10-25 14:50')

class ShareEditForm(forms.Form):
    passenger = forms.IntegerField(label='Number of Passengers', validators=[MaxValueValidator(200),MinValueValidator(1)])

class PasswordForm(forms.Form):
    oldpassword = forms.CharField(label='Old Password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='New Password Confirmation', widget=forms.PasswordInput)
    
    def clean_oldpassword(self):
        oldpassword = self.cleaned_data.get('oldpassword')

        if len(oldpassword) < 8:
            raise forms.ValidationError("Old password should be at least 8 characters.")
        elif len(oldpassword) > 20:
            raise forms.ValidationError("Old password cannot exceed 20 characters.")
        
        return oldpassword

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if len(password1) < 8:
            raise forms.ValidationError("Password should be at least 8 characters.")
        elif len(password1) > 20:
            raise forms.ValidationError("Password cannot exceed 20 characters.")
        
        return password1
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password mismatch. Please enter again.")

        return password2

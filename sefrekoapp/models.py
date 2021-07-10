from typing_extensions import Required
from django.db import models
from django.db import forms
from public_view.models import *
from django.contrib.auth.models import User
from django.core import validators
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.template.defaultfilters import slugify
from django.core.validators import RegexValidator
# To use the MoneyField below:
# Install it using '$ pip install django-money'
# Then add 'djmoney' to your installed app so that money field 
# are displayed correctly in the admin.
from djmoney.models.fields import MoneyField
# Create your models here.


class Auto_Maker(models.Model):
    make = models.CharField(max_length=25, null=False)
    created_by = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.make
    

class Auto_Model(models.Model):
    # Link auto-model to the maker/manufacturer
    make = models.ForeignKey(Auto_Maker, on_delete=models.CASCADE)
    model_name = models.CharField(max_length=25, null=False)
    def __str_(self):
        return self.model_name
        
class vehicle (models.Model):    
    #This table or model stores information about each vehicle registered on this platform

    #These are they types/design of vehicles that user will choose from
    Coupe = 'Coupe'
    Full_size_van = 'Full Size Van'
    Hatch_back = 'Hatch Back'
    Mini_Truck = 'Mini Truck'
    Mini_Van = 'Mini Van'
    Sedan = 'Sedan'
    SUV = 'SUV'
    Tractor = 'Tractor'
    Truck = 'Truck'
    Wagon = 'Wagon'

    # Variables for fuel type
    Diesel = 'Diesel'
    Electric = 'Electric'
    Hybrid = 'Hybrid'
    Hydrogen_Fuel_Cell = 'Hydrogen Cell'
    Petrol = 'Petrol'

    #Transmission type
    Manual = 'Manual'
    Automatic = 'Automatic'

    #Usage status
    Brand_New = 'Brand New'
    Foreign_Used = 'Foreign Use'
    Local_Used = 'Naija Used'   

    #drive train type
    AWD = 'All Wheel Drive'
    FWD = 'Front Wheel Drive'
    F4WD = '4 Wheel Drive'
    RWD = 'Rear Wheel Drive'

    


    #These variables are the choices for the vehicle availability status
    Available = 'Available'
    Black_List = 'Black List'
    Sold = 'Sold'
    Suspend = 'Suspend'
    Verified = 'Verified'



    Choose = ''


    body_type =[
        (Coupe, 'Coupe'),
        (Full_size_van, 'Full Size Van'),
        (Hatch_back, 'Hatch Back'),
        (Mini_Truck, 'Mini Truck'),
        (Mini_Van, 'Mini Van'),
        (Sedan, 'Sedan'),
        (SUV, 'SUV'),
        (Tractor, 'Tractor'),
        (Truck, 'Truck'),
        (Wagon, 'Wagon')
        (Choose, 'Choose your prefered type:')

    ]

    fuel_type =[
        (Diesel, 'Diesel'),
        (Electric, 'Electric'),
        (Hybrid, 'Hybrid'),
        (Hydrogen_Fuel_Cell, 'Hydrogen Fuel Cell'),
        (Petrol, 'Petrol'),
        (Choose, 'Choose the type of fuel'),
    ]

    use_status =[
        (Brand_New, 'Brand New'),
        (Foreign_Used, 'Foreign Use'),
        (Local_Used, 'Naija Used'),
    ]

    transmission_type =[
        (Automatic, 'Automatic Transmission'),
        (Manual, 'Manual Transmission'),
        (Choose, 'Choose type')

    ]

    listing_status =[
        (Available, 'Available'),
        (Black_List, 'Black List'),
        (Sold, 'Sold'),
        (Verified, 'Verified'),
        Verified, 
    ]

    drivetrain =[
        (AWD, 'All Wheel Drive'),
        (FWD, 'Front Wheel Drive'),
        (F4WD, '4 Wheel Drive'),
        (RWD, 'Rear Wheel Drive'),
        (Choose, 'Choose vehicle drive train'),

    ]

    # Link vehicle to the model type
    vehicle_model = models.ForeignKey(Auto_Model, on_delete=models.CASCADE)
    # Generate the vehicle's model year as a selectable integer and store it in a combo box
    VIN = models.CharField(max_length=25, widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'Vehicle Identification Number/Chasis Number'} ))
    
    YEAR_CHOICES = [(r,r) for r in range(1985, datetime.date.today().year+1)]
    model_year = models.IntegerField(_('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    
    body_style = models.CharField(max_length=25, choices=body_type, default='Choose')
    vehicle_colour = models.CharField(max_length=25)
    fuel = models.CharField(max_length=15,choices=fuel_type, default='Choose')
    transmission = models.CharField(max_length=25,choices=transmission_type, default='Choose')
    drive_train = models.CharField(max_length=25, choices=drivetrain, default='Choose')
    Odometer = models.IntegerField(Required=False, null=True)
    vehicle_status = models.CharField(max_length=25, choices=use_status, default='Choose')

    vehicle_location = models.TextField(blank=True, null=True)
    posted_by = models.ForeignKey(User)
    listing_price = models.MoneyField(max_digits=14, decimal_places=2, default_currency='NGN')
    start_display_on = models.DateField()
    status = models.CharField(max_length=25,choices=vehicle_status,default='Choose') 
    posted_on = models.DateTimeField(auto_now=True)

# The function below uses the slug field to uniquely identify
# all the pictures for each vehicle. 
def get_image_filename(instance, filename):
    title = instance.vehicle.VIN
    slug = slugify(title)
    return "vehicle_images/%s-%s" %(slug, filename)

# create the model to store the multiple images url for each vehicle.
class vehicle_image(models.Model):
    vehicle = models.ForeignKey(vehicle, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Image')


class Seller(models.Model):
    seller_name = models.CharField(max_length=35)
    company = models.CharField(max_length=50, Required=False)
    email = models.EmailField()
    profile_image = models.ImageField(blank=True, null=True, upload_to='uploads/Seller_profiles')
    contact_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.seller_name


class PhoneNumber(models.Model):
    user_id = models.ForeignKey(Seller, related_name='phone_number', on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list

    def __str__(self):
        return self.clean
    

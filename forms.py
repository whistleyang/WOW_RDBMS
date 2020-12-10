from django import forms
from .models import Customer, Indi_cust, Corp_cust, Payment
from .models import Rental_Record
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'password']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['fname', 'lname', 'country', 'state', 'city',
             'street', 'zipcode', 'email', 'phone', 'cust_type']

class Indi_CustForm(forms.ModelForm):
    class Meta:
        model = Indi_cust
        fields = ['dl_num', 'insur_com_name', 'insur_polic_num']

class Corp_custForm(forms.ModelForm):
    class Meta:
        model = Corp_cust
        fields = ['employee_id', 'corp']

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['make','model','year','vin','class_id',
                  'location_id','lp_num']

class RecordForm(forms.ModelForm):
    class Meta:
        model = Rental_Record
        fields = ['customer', 'pickup_date', 'dropoff_date', 'start_odo',
            'end_odo', 'odo_limit', 'vehicle', 'pu_location', 'do_location' ]
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date'}),
            'dropoff_date': forms.DateInput(attrs={'type': 'date'})
        }

from django import forms
from .models import Customer
from .models import Employee, Rental_Record
from django.contrib.auth.models import User

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['eid','ename','eemail', 'econtact']

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

class RecordForm(forms.ModelForm):
    class Meta:
        model = Rental_Record
        fields = ['record_id', 'pickup_date', 'dropoff_date', 'start_odo',
            'end_odo', 'odo_limit', 'vehicle', 'pu_location', 'do_location' ]
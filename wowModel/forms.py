from django import forms
from .models import Customer
from .models import Employee
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
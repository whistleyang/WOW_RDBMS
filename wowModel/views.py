from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, CustomerForm, RecordForm, Indi_CustForm, Corp_custForm
from .models import Rental_Record, Customer
from django.contrib import auth
# Create your views here.

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('/cust_details/'+str(customer.customer_id))
    else:
        user_form = UserForm()
        customer_form = CustomerForm()
    return render(request, 'register.html', 
        {'user_form':user_form, 'customer_form':customer_form})

def cust_details(request, id):
    registered = False
    customer = Customer.objects.get(customer_id=id)
    if customer.cust_type == 'I':
        form = Indi_CustForm()
    else:
        form = Corp_custForm()
    if request.method == "POST":
        if customer.cust_type == 'I':
            form = Indi_CustForm(request.POST)
        else:
            form = Corp_custForm(request.POST)
        if form.is_valid():
            cust = form.save(commit=False)
            cust.customer = customer
            cust.save()
            registered = True
    return render(request, 'cust_details.html', 
        {'form':form, 'registered':registered})
    

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_obj = auth.authenticate(username=username, password=password)
        if user_obj:
            auth.login(request, user_obj)
            path = request.GET.get("next") or "/show"
            return redirect(path)
        else:
            return redirect('/accounts/login/')
    return render(request, 'login.html')

@login_required
def emp(request):
    if request.method == "POST":
        #form = EmployeeForm(request.POST)
        form = RecordForm(request.POST)
        if form.is_valid():
            try:
                empl = form.save(commit=False)
                empl.user = request.user
                form.save()
                return redirect('/show')
            except:
                pass
    else:
        #form = EmployeeForm()
        form = RecordForm()
    return render(request, 'add_emp.html', {'form':form})

@login_required
def show(request):
    if request.user.is_superuser:
        #employees = Employee.objects.all()
        records = Rental_Record.objects.all()
    else:
        #employees = Employee.objects.filter(user=request.user)
        records = Rental_Record.objects.filter(user=request.user)
    #return render(request, "show.html", {'employees': employees})
    return render(request, 'show.html', {'records':records})

@login_required
def edit(request, id):
    #employee = Employee.objects.get(id=id)
    record = Rental_Record.objects.get(record_id=id)
    #return render(request, 'edit.html', {'employee':employee})
    return render(request, 'edit.html', {'record':record})

@login_required
def update(request, id):
    #employee = Employee.objects.get(id=id)
    #form = EmployeeForm(request.POST, instance=employee)
    record = Rental_Record.objects.get(record_id=id)
    form = RecordForm(request.POST, instance=record)
    if form.is_valid():
        form.save()
        return redirect("/show")
    #return render(request, "edit.html", {'employee:employee'})
    return render(request, 'edit.html', {'form': form})

@login_required
def destroy(request, id):
    #employee = Employee.objects.get(id=id)
    #employee.delete()
    record = Rental_Record.objects.get(record_id=id)
    record.delete()
    return redirect("/show")

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/accounts/login/')


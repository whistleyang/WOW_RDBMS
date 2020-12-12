from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm, CustomerForm, RecordForm, Indi_CustForm, Corp_custForm,VehicleForm
from .models import Rental_Record, Customer, Indi_cust, Corp_cust, \
     Veh_class, Vehicle, Invoice, Payment, Location
from django.contrib import auth
from django.utils import timezone
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
def profile(request):
    info = Customer.objects.get(user=request.user)
    indi = False
    if info.cust_type == 'I':
        indi = True
        details = Indi_cust.objects.get(customer=info)
    else:
        details = Corp_cust.objects.get(customer=info)
    return render(request, 'profile.html', 
        {'info':info, 'details':details, 'indi':indi})

@login_required
def edit_profile(request):
    customer = Customer.objects.get(user=request.user)
    cust_form = CustomerForm(request.POST, instance=customer)
    if customer.cust_type == 'I':
        detail = Indi_cust.objects.get(customer=customer)
        detail_form = Indi_CustForm(request.POST, instance=detail)
    else:
        detail = Corp_cust.objects.get(customer=customer)
        detail_form = Corp_custForm(request.POST, instance=detail)
    if cust_form.is_valid() and detail_form.is_valid():
        cust = cust_form.save(commit=False)
        cust.user = request.user
        cust.save()
        detail = detail_form.save(commit=False)
        detail.customer = cust
        detail.save()
        return redirect('/info')
    return render(request, 'edit_profile.html', 
        {'cust_form':cust_form, 'detail_form':detail_form})

@login_required
def add_record(request):
    # employee auth
    customers = Customer.objects.all()
    vehicles = Vehicle.objects.all()
    locations = Location.objects.all()
    if request.method == "POST":
        form = RecordForm(request.POST)
        if form.is_valid():
            try:
                record = form.save(commit=False)
                customer = record.customer
                record.user = customer.user
                form.save()
                return redirect('/show')
            except:
                pass
    else:
        form = RecordForm()
    return render(request, 'add_emp.html', {'form': form, 
        'customers':customers, 'vehicles':vehicles, 'locations':locations})

@login_required
def show(request):
    if request.user.is_superuser:
        records = Rental_Record.objects.all()
    else:
        records = Rental_Record.objects.filter(user=request.user)
    return render(request, 'show.html', {'records':records})


@login_required
def update(request, id):
    # employee auth
    customers = Customer.objects.all()
    vehicles = Vehicle.objects.all()
    locations = Location.objects.all()
    record = Rental_Record.objects.get(record_id=id)
    form = RecordForm(request.POST, instance=record)
    if form.is_valid():
        form.save()
        return redirect("/show")
    return render(request, 'edit.html', {'form': form, 
        'customers':customers, 'vehicles':vehicles, 'locations':locations})

@login_required
def destroy(request, id):
    # employee auth
    record = Rental_Record.objects.get(record_id=id)
    record.delete()
    return redirect("/show")

@login_required
def vehicle_add(request):
    if request.method =="POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/vehi_show')
    else:
        form = VehicleForm()
    return render(request, 'vehicle_add.html',{'form':form})

@login_required
def vehicle_show(request):
    records = Vehicle.objects.all()
    return render(request, 'vehicle_show.html', {'records':records})

@login_required
def vehicle_update(request, id):
    # employee auth
    record = Vehicle.objects.get(vehicle_id=id)
    form = VehicleForm(request.POST, instance=record)
    if form.is_valid():
        form.save()
        return redirect("/vehi_show")
    return render(request, 'vehicle_edit.html', {'form': form})

@login_required
def vehicle_destroy(request, id):
    # employee auth
    record = Vehicle.objects.get(vehicle_id=id)
    record.delete()
    return redirect("/vehi_show")

@login_required
def gene_invoice(request, id):
    # we need a new web to list invoice
    record = Rental_Record.objects.get(record_id=id)
    idate = timezone.localtime()
    try:
        invoice = Invoice.objects.get(record=record)
        invoice.idate=idate
        invoice.save()
    except:
        vehicle = record.vehicle
        veh_class = vehicle.class_id
        rent_duration = (record.dropoff_date - record.pickup_date).days
        overfee = 0
        if record.odo_limit:
            total_odo = record.end_odo - record.start_odo
            if total_odo > rent_duration * record.odo_limit:
                overfee = veh_class.fees * \
                    (total_odo - rent_duration * record.odo_limit)
        amount = rent_duration * veh_class.rental_rate + overfee
        invoice = Invoice.objects.create(idate=idate, amount=amount, record=record)
    # add discount


    # create payment and redirect to payment page
    if request.method == "POST":
        method = request.POST.get("method")
        card_num = request.POST.get("card_num")
        pdate = timezone.localtime()
        customer = record.customer
        payment = Payment.objects.create(customer=customer, pdate=pdate,
            method=method, card_num=card_num, invoice=invoice)
        # after payment, we need to delete this record
        return render(request, 'payment.html', {'payment': payment})

    return render(request, 'invoice.html', {'invoice': invoice})

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/accounts/login/')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmployeeForm
from .models import Employee
from django.contrib import auth
# Create your views here.

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
            redirect('accounts/login/')
    return render(request, 'login.html')

@login_required
def emp(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                empl = form.save(commit=False)
                empl.user = request.user
                form.save()
                return redirect('/show')
            except:
                pass
    else:
        form = EmployeeForm()
    return render(request, 'index.html', {'form':form})

@login_required
def show(request):
    if request.user.is_superuser:
        employees = Employee.objects.all()
    else:
        employees = Employee.objects.filter(user=request.user)
    return render(request, "show.html", {'employees': employees})

@login_required
def edit(request, id):
    employee = Employee.objects.get(id=id)
    return render(request, 'edit.html', {'employee':employee})

@login_required
def update(request, id):
    employee = Employee.objects.get(id=id)
    form = EmployeeForm(request.POST, instance=employee)
    if form.is_valid():
        form.save()
        return redirect("/show")
    return render(request, "edit.html", {'employee:employee'})

@login_required
def destroy(request, id):
    employee = Employee.objects.get(id=id)
    employee.delete()
    return redirect("/show")

@login_required
def logout(request):
    auth.logout(request)
    return redirect('accounts/login/')


from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse
from django.urls import reverse_lazy
from employee.forms import UserForm
from ems.decorators import role_required, admin_only
from . models import *

def user_login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if request.GET.get('next', None):
                return HttpResponseRedirect(request.GET['next'])
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            context['error'] = 'Username or password is invalid !!!'
            return render(request, 'auth/login.html', context)
    else:
        return render(request, 'auth/login.html', context)


@login_required(login_url="/login/")
def success(request):
    context = {}
    context['user'] = request.user
    return render(request, 'auth/success.html', context)


def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponseRedirect(reverse('user_login'))

@login_required(login_url="/login/")
def employee_list(request):
    uf = UserForm()
    context = {}
    context['us'] = User.objects.all()
    context['title'] = 'Employees'
    context['uf']=uf
    return render(request, 'employee/index.html', context)

@login_required(login_url="/login/")
def employee_details(request, id:None):
    context = {}
    context['ur'] = get_object_or_404(User, id=id)
    return render(request, 'employee/details.html', context)

@login_required(login_url="/login/")
@role_required(allowed_roles=["Admin", "HR"])
def employee_add(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)
        if uf.is_valid():
            uf.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request, 'employee/add.html', {'uf': uf})
    else:
        uf = UserForm()
        return render(request, 'employee/add.html', {'uf': uf})

@login_required(login_url="/login/")
def employee_edit(request, id):
    u = get_object_or_404(User, id=id)
    if request.method == 'POST':
        uf = UserForm(request.POST, instance=u)
        if uf.is_valid():
            uf.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request, 'employee/edit.html', {'uf': uf})
    else:
        uf = UserForm(instance=u)
        return render(request, 'employee/edit.html', {'uf': uf})

@login_required(login_url="/login/")
def employee_delete(request, id):
    u = get_object_or_404(User, id=id)
    if request.method == 'POST':
        u.delete()
        return HttpResponseRedirect(reverse('employee_list'))
    else:
        context = {}
        context['u'] = u
        return render(request, 'employee/delete.html', context)


def auth_employee_add(request):
    if request.method == 'POST':
        print('\n\n post method')
        user_create=User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],username= request.POST['username'],email=request.POST['email'],password=request.POST['password'])
        user_create.save()
        pro=Profile()
        pro.usr=user_create
        pro.designation=request.POST['designation']
        pro.save()
        print('\n\nuser created successfully')
        print("usercreated")
        return redirect('/')
    else:
        print('\n\n not a post method')
        uf = UserForm()
        return render(request, 'employee/add.html', {'uf': uf})

class ProfileUpdate(UpdateView):
    fields = ['designation', 'salary']
    template_name = 'auth/profile_update.html'
    success_url = reverse_lazy('my_profile')

    def get_object(self):
        return self.request.user.profile

class MyProfile(DetailView):
    template_name = 'auth/profile.html'

    def get_object(self):
        return self.request.user.profile



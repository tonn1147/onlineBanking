from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpRequest
from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from typing import Any
from django.core.paginator import Paginator,PageNotAnInteger
from django.urls import reverse,resolve
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.contrib.auth.models import Group,Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

from .forms import SignupForm
from .models import CustomUser,Account,Transaction
# Create your views here.

def login(request: HttpRequest):
    if request.method == "POST":
        email: str = request.POST.get("email")
        password: str = request.POST.get("password")

        try:
            user = CustomUser.objects.first(email=email)
            if not user: raise ValueError()
            user = authenticate(request,email=email,password=password)

            if user is not None:
                login(request,user)
                return redirect('home')
        except ValueError:
            messages.error(request,"incorrect email or password")
    return render(request,'main/login.html',context=None)

def signup(request: HttpRequest):
    form: SignupForm = SignupForm()

    if request.user.is_authenticated:
        home_url = reverse('home')
        return redirect(home_url)

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user: CustomUser = form.save()

            # Get the `user` group, or create it if it doesn't exist.
            user_group: QuerySet = Group.objects.get("user")
            if not user_group.exists():
                user_group: Group = Group.objects.create("user")

                # Create permissions for viewing and creating transactions and accounts.
                pm_models = [Transaction, Account]
                for pm_model in pm_models:
                    content_type: ContentType = ContentType.objects.get_for_model(pm_model)
                    view_pm: Permission = Permission.objects.create(
                        codename=f'view_{pm_model._meta.model_name}',
                        content_type=content_type
                    )
                    create_pm: Permission = Permission.objects.create(
                        codename=f'create_{pm_model._meta.model_name}',
                        content_type=content_type
                    )
                    user_group.permissions.add(view_pm)
                    user_group.permissions.add(create_pm)

            # Add the user to the `user` group.
            user.groups.add(user_group)

            # Log in the user and redirect them to the home page.
            login(request, user)
            return redirect('home')

    context = {"form": form}
    return render(request,"main/signup.html",context=context)

@login_required(login_url='login')
def home(request : HttpRequest):
    raise NotImplementedError()

@login_required(login_url='login')
def create_account(request: HttpRequest):
    raise NotImplementedError()

@login_required(login_url='login')
def view_account(request: HttpRequest):
    raise NotImplementedError()

@login_required(login_url='login')
def create_transaction(request: HttpRequest):
    raise NotImplementedError()

@login_required(login_url='login')
def view_transaction(request: HttpRequest):
    raise NotImplementedError()

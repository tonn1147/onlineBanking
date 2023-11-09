from django.http import HttpResponse,Http404,HttpRequest
from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from typing import Any
from django.db import transaction
from django.core.paginator import Paginator,PageNotAnInteger
from django.urls import reverse,resolve
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.contrib.auth.models import Group,Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from decimal import Decimal

from .forms import SignupForm,TransactionForm
from .models import CustomUser,Account,Transaction
# Create your views here.

def login_page(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email: str = request.POST.get("email")
        password: str = request.POST.get("password")

        try:
            user = CustomUser.objects.filter(email=email)
            if not user.exists(): raise ValueError()
            user = authenticate(request,email=email,password=password)

            if user is not None:
                login(request,user=user)
                return redirect('home')
            else:
                messages.warning(request,"incorrect email or password")
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
            with transaction.atomic():
                user: CustomUser = form.save()

                # Get the `user` group, or create it if it doesn't exist.
                user_group: Group = Group.objects.get_or_create(name="user")
                if user_group[1]:
                    # Create permissions for viewing and creating transactions and accounts.
                    pm_models = [Transaction, Account]
                    for pm_model in pm_models:
                        content_type: ContentType = ContentType.objects.get_for_model(pm_model)
                        view_pm: Permission = Permission.objects.get_or_create(
                            codename=f'view_{pm_model._meta.model_name}',
                            content_type=content_type
                        )
                        create_pm: Permission = Permission.objects.get_or_create(
                            codename=f'add_{pm_model._meta.model_name}',
                            content_type=content_type
                        )
                        user_group[0].permissions.add(view_pm[0])
                        user_group[0].permissions.add(create_pm[0])

                # Add the user to the `user` group.
                user.is_active = False
                user.save(force_update=True)
                user.groups.add(user_group[0])

                # Log in the user and redirect them to the home page.
                return redirect('login')
    
    context = {"form": form}
    return render(request,"main/signup.html",context=context)

@login_required(login_url='login')
def home(request : HttpRequest):
    if not request.user.is_active: return HttpResponse("waiting for activating account")

    accounts = Account.objects.all()
    if request.method == "POST":
        if request.POST.get("create-account") == "create":
            user_id = request.user.id
            Account.objects.create(user_id=user_id)
            return redirect(request.path_info)
    
    context = {"accounts": accounts}
    return render(request,"main/home.html",context=context)

@login_required(login_url='login')
def view_account(request: HttpRequest,slug: str):
    try:
        account = Account.objects.get(slug=slug)
    except:
        raise Http404
    
    from_account_transaction: QuerySet = account.transaction_set.filter(from_account=slug).values_list("from_account","to_account","money_transfer","detail","date")
    to_account_transaction: QuerySet = account.transaction_set.filter(to_account=slug).values_list("from_account","to_account","money_transfer","detail","date")
    transactions: QuerySet = from_account_transaction.union(to_account_transaction).order_by("date")
    
    context = {"account": account,"transactions": transactions}
    return render(request,"main/account.html",context=context)

@login_required(login_url='login')
def create_transaction(request: HttpRequest,id: str):
    try:
        account: Account = Account.objects.get(slug=id)
    except:
        raise Http404
    
    initial_data = {"from_account": id}
    form: TransactionForm = TransactionForm(initial=initial_data)

    if request.method == "POST":
        form: TransactionForm = TransactionForm(request.POST)
        if form.is_valid():
            from_account: str = form.cleaned_data["from_account"]
            to_account: str = form.cleaned_data["to_account"]
            money_transfer: Decimal = form.cleaned_data["money_transfer"]
            detail: str = form.cleaned_data["detail"]
            try:
                payer: Account = Account.objects.select_for_update().get(account_id=from_account)
                payee: Account = Account.objects.select_for_update().get(account_id=to_account)
                
                with transaction.atomic():
                    payer.current_balance -= money_transfer
                    payer.save()

                    payee.current_balance += money_transfer
                    payee.save()
                    return redirect("account",slug=id)
            except:
                messages.error(request,"wrong account id!")
            
    context = {"account": account,"form": form}
    return render(request,"main/transaction.html",context=context)

from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpRequest
from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from typing import Any
from django.core.paginator import Paginator,PageNotAnInteger
from django.urls import reverse,resolve
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def login(request: HttpRequest):
    raise NotImplementedError()

def signup(request: HttpRequest):
    raise NotImplementedError()

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

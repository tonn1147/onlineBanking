from django.urls import path, include

from main import views
urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login_page,name='login'),
    path('signup/',views.signup,name='signup'),
    path('account/<slug:slug>',views.view_account,name="account"),
    path("account/<slug:slug>/create_transaction",views.create_transaction,name="create_transaction"),
]
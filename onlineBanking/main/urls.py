from django.urls import path, include

from main import views
urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login_page,name='login'),
    path('signup/',views.signup,name='signup')
]
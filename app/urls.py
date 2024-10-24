
from django.urls import path
from app.views import registration,login_page,home_page,logout_page

urlpatterns = [
    path('register/',registration,name='register'),
    path('login/',login_page,name='loginpage'),
    path('home/',home_page,name='home'),
    path('logout/',logout_page,name='logout')
]

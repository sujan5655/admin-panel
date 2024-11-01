
from django.urls import path
from app.views import registration,login_page,home_page,logout_page,seller_dashboard,add_property,update_property,property_detail,book_property,update_booking_status,seller_bookings,approve_booking,Properties,booking_list

urlpatterns = [
    path('register/',registration,name='register'),
    path('login/',login_page,name='loginpage'),
    path('home/',home_page,name='home'),
    path('logout/',logout_page,name='logout'),
    path('seller/', seller_dashboard, name='seller'),
    path('add/',add_property,name='addproperty'),
    path('update/<int:id>/',update_property,name='update'),
   

    path('property/', Properties, name='allproperties'),

    path('property/<int:property_id>/', property_detail, name='property_detail'),
    path('book/<int:property_id>/', book_property, name='book_property'),
      path('seller/bookings/', seller_bookings, name='seller_bookings'),
      path('seller/bookings/<int:booking_id>/<str:status>/', update_booking_status, name='update_booking_status'),
       path('property/<int:property_id>/book/', book_property, name='book_property'),
       path('bookings/<int:id>/approve/', approve_booking, name='approve_booking'),
         path('bookings/', booking_list, name='booking_list'),
         path('bookings/<int:id>/reject/',approve_booking,name='reject_booking')
]

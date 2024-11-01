from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Property, Booking
from .forms import PropertyForm


def registration(request):
    error = None
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            error = "Username already exists"
        else:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
            return redirect("/login")
    context = {
        'error': error
    }
    return render(request, 'registrationPage.html', context)

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/seller')
    return render(request, 'loginPage.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)  
    return redirect('/login')  

def home_page(request):
    return render(request, 'home.html')

from django.contrib.auth.decorators import login_required

@login_required
def seller_dashboard(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        seller_id = request.user.id
        properties=Property.objects.all()
        # Proceed with your logic here
        # For example, fetching seller's properties, bookings, etc.
        context={
         'seller_id':seller_id,
         'properties':properties
        }
        return render(request, 'seller_dashboard.html', {'seller_id': seller_id})
    else:
        # Redirect to login page if the user is not authenticated
        return redirect('loginpage')
    
from django.shortcuts import render, redirect
from .forms import PropertyForm
from .models import Property

from django.shortcuts import render, redirect
@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.seller = request.user
            # Set availability based on checkbox
            is_available = request.POST.get('is_available')
            property.is_available = True if is_available == "on" else False
            property.save()
            return redirect('allproperties')  # Redirect to avoid resubmission on page refresh
    else:
        form = PropertyForm()
    return render(request, 'add_property.html', {'form': form})


from django.shortcuts import get_object_or_404, redirect, render
from .forms import PropertyForm
from .models import Property

from django.shortcuts import get_object_or_404, redirect, render
from .forms import PropertyForm
from .models import Property

def update_property(request, id):
    # Get the property instance by ID
    property = get_object_or_404(Property, id=id)

    if request.method == "POST":
        # Bind form with POST data and instance to update
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            updated_property = form.save(commit=False)
            
            # Set the seller to the current user (ensuring it's a User instance)
            updated_property.seller = request.user
            
            # Update availability based on checkbox
            is_available = request.POST.get('is_available')
            updated_property.is_available = True if is_available == "on" else False
            
            # Save the updated property instance
            updated_property.save()
            return redirect('seller')  # Redirect to the seller dashboard
            
    else:
        form = PropertyForm(instance=property)
    
    context = {
        'form': form
    }
    return render(request, 'update_property.html', context)


from django.shortcuts import get_object_or_404, redirect, render
from .models import Property, Booking
from django.contrib.auth.decorators import login_required

# @login_required
# def book_property(request, property_id):
#     property = get_object_or_404(Property, id=property_id, is_available=True)
    
#     # Check if the user already has a pending booking for this property
#     if Booking.objects.filter(property=property, client=request.user, approval_status='pending').exists():
#         # Redirect to a page with a message if booking already exists
#         return redirect('property_detail', property_id=property.id)

#     # Create a new booking
#     Booking.objects.create(property=property, client=request.user, is_booked=True)
#     return redirect("% url 'properties'%", property_id=property.id)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Booking, Property
from django.contrib import messages



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Booking

@login_required
@login_required
def approve_booking(request, id):
    # Fetch the booking object
    booking = get_object_or_404(Booking, id=id)

    if request.method == "POST":
        # Get the selected approval_status from the form
        approval_status = request.POST.get("status")
        
        # Check if the selected approval_status is valid
        if approval_status in ["approved", "rejected"]:
            booking.approval_status = approval_status
            booking.save()
            messages.success(request, f"The booking has been {approval_status} successfully.")
            return redirect('seller_bookings')
        else:
            messages.error(request, "Invalid status selected.")

    # Render the template with the booking details
    return render(request, 'approve_booking.html', {'booking': booking})



@login_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, property__seller=request.user)
    
    # Reject the booking
    booking.approval_status = 'rejected'
    booking.save()
    return redirect('seller_bookings')  # Redirect to seller's booking list

from django.shortcuts import render, get_object_or_404
from .models import Property, Booking
from django.contrib.auth.decorators import login_required

@login_required
def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    booking = None

    # Check if the user has a booking for this property
    if request.user.is_authenticated:
        booking = Booking.objects.filter(property=property, client=request.user).first()

    context = {
        'property': property,
        'booking': booking,
        'is_available': property.is_available and (booking is None or booking.approval_status == 'rejected'),
    }
    return render(request, 'property_detail.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Property, Booking
from django.contrib.auth.decorators import login_required

@login_required
def seller_bookings(request):
    # Fetch properties listed by the logged-in seller
    properties = Property.objects.filter(seller=request.user)
    
    # Retrieve all bookings related to these properties
    bookings = Booking.objects.filter(property__in=properties)

    context = {
        'bookings': bookings,
    }
    return render(request, 'seller_bookings.html', context)


@login_required
def update_booking_status(request, booking_id, status):
    booking = get_object_or_404(Booking, id=booking_id, property__seller=request.user)
    if status in ['approved', 'rejected']:
        booking.approval_status = status
        booking.save()
    return redirect('seller_bookings')

@login_required
def book_property(request, property_id):
    property = get_object_or_404(Property, id=property_id, is_available=True)

    if request.method == 'POST':
        # Check if the user already has a pending booking
        if Booking.objects.filter(property=property, client=request.user, approval_status='pending').exists():
            messages.warning(request, "You already have a pending booking for this property.")
            return redirect('/property/')

        # Create a new booking
        booking = Booking(property=property, client=request.user)
        booking.save()

        messages.success(request, "Your booking request has been submitted successfully!")
        return redirect('/property/')

    return render(request, 'book_property.html', {'property': property})

def Properties(request):
    property=Property.objects.all()
    context={
        'property':property
    }
    return render(request,'Property.html',context)

def booking_list(request):
    bookings = Booking.objects.all()  # Retrieve all bookings, or filter by user if needed
    return render(request, 'booking_list.html', {'bookings': bookings})


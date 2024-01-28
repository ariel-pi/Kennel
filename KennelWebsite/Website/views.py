from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import BoardingHouse, Booking
from .forms import BookingForm ,UserProfileForm, BoardingHouseForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseBadRequest
from .forms import RegistrationForm
from django.contrib.auth import login


def home(request):
    return render(request, 'home.html')

def boardinghouse_list(request):
    boardinghouses = BoardingHouse.objects.all()
    return render(request, 'boardinghouse_list.html', {'boardinghouses': boardinghouses})

def boardinghouse_detail(request, boardinghouse_id):
    boardinghouse = BoardingHouse.objects.get(id=boardinghouse_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.boarding_house = boardinghouse
            booking.save()
            messages.success(request, 'Booking request sent successfully!')
            return redirect('boardinghouse_list')
    else:
        form = BookingForm()

    return render(request, 'boardinghouse_detail.html', {'boardinghouse': boardinghouse, 'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})
def custom_logout(request):
    logout(request)
    return redirect('Website:home')  # Redirect to the home page of the 'Website' app
@login_required
def booking_history(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking_history.html', {'bookings': bookings})

@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {'form': form})


@login_required
def owner_dashboard(request):
    user = request.user
    boarding_houses = BoardingHouse.objects.filter(user=user)
    bookings = Booking.objects.filter(boarding_house__in=boarding_houses)

    context = {'bookings': bookings}
    return render(request, 'owner_dashboard.html', context)

@login_required
def update_booking_status(request, booking_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Booking.STATUS_CHOICES):
            booking = Booking.objects.get(id=booking_id)
            booking.status = new_status
            booking.save()
            return redirect('owner_dashboard')
    return HttpResponseBadRequest('Invalid form submission')

@login_required
def add_boardinghouse(request):
    if request.method == 'POST':
        form = BoardingHouseForm(request.POST)
        if form.is_valid():
            boardinghouse = form.save(commit=False)
            # Assuming you want to associate the new boardinghouse with the logged-in user
            boardinghouse.user = request.user
            boardinghouse.user = request.user  # Set the user field
            boardinghouse.save()
            return redirect('boardinghouse_list')  # Redirect to the list of boardinghouses after successful addition
    else:
        form = BoardingHouseForm()

    return render(request, 'add_boardinghouse.html', {'form': form})

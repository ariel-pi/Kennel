# views.py
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import BoardingHouse, Booking
from .forms import BookingForm,  BoardingHouseForm, RegistrationForm #,UserProfileForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')

class BoardinghouseListView(View):
    def get(self, request, *args, **kwargs):
        boardinghouses = BoardingHouse.objects.all()
        return render(request, 'boardinghouse_list.html', {'boardinghouses': boardinghouses})

class BoardinghouseDetailView(View):
    def get(self, request, boardinghouse_id, *args, **kwargs):
        boardinghouse = get_object_or_404(BoardingHouse, id=boardinghouse_id)
        form = BookingForm()

        return render(request, 'boardinghouse_detail.html', {'boardinghouse': boardinghouse, 'form': form})

    def post(self, request, boardinghouse_id, *args, **kwargs):
        boardinghouse = get_object_or_404(BoardingHouse, id=boardinghouse_id)
        form = BookingForm(request.POST)

        if form.is_valid():
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']

            # Perform any additional validation or processing here

            # Create a Booking instance
            booking = Booking.objects.create(
                user=request.user,
                boarding_house=boardinghouse,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                status='pending'  # You may set the initial status as needed
            )

            messages.success(request, 'Booking successful! Check your booking history for details.')
            return redirect('boardinghouse_list')

        # If form is not valid, re-render the page with the form and error messages
        return render(request, 'boardinghouse_detail.html', {'boardinghouse': boardinghouse, 'form': form})

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'registration/register.html', {'form': form})

class BookingHistoryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        bookings = Booking.objects.filter(user=request.user)
        return render(request, 'booking_history.html', {'bookings': bookings})

class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = UserProfileForm(instance=request.user.profile)
        return render(request, 'profile.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')
        return render(request, 'profile.html', {'form': form})

class OwnerDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Boardinghouse Owner').exists()

    def get(self, request, *args, **kwargs):
        user = request.user
        boarding_houses = BoardingHouse.objects.filter(user=user)
        bookings = Booking.objects.filter(boarding_house__in=boarding_houses)
        context = {'bookings': bookings}
        return render(request, 'owner_dashboard.html', context)

class UpdateBookingStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Boardinghouse Owner').exists()

    def post(self, request, booking_id, *args, **kwargs):
        new_status = request.POST.get('status')
        if new_status in dict(Booking.STATUS_CHOICES):
            booking = Booking.objects.get(id=booking_id)
            booking.status = new_status
            booking.save()
            return redirect('owner_dashboard')
        return HttpResponseBadRequest('Invalid form submission')

class AddBoardinghouseView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name='Boardinghouse Owner').exists()

    def get(self, request, *args, **kwargs):
        form = BoardingHouseForm()
        return render(request, 'add_boardinghouse.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = BoardingHouseForm(request.POST)
        if form.is_valid():
            boardinghouse = form.save(commit=False)
            boardinghouse.user = request.user
            boardinghouse.save()
            return redirect('boardinghouse_list')
        return render(request, 'add_boardinghouse.html', {'form': form})

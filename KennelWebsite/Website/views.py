# views.py
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import BoardingHouse, Booking, Profile, Review
from .forms import BookingForm,  BoardingHouseForm, RegistrationForm ,ProfileForm
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import UpdateUsernameForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .forms import UpdateUsernameForm, UpdatePasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html')
    
class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # create a profile instance for the user
            Profile.objects.create(user=user)
            return redirect('home')
        return render(request, 'registration/register.html', {'form': form})

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile
        form = ProfileForm(instance=profile)
        return render(request, 'profile.html', {'form': form, 'profile': profile})

    def post(self, request):
        #TODO: remove the profile picture if the user wants to
        # or if the user wants to update the profile picture
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'profile.html', {'form': form})

class UpdateUsernameView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'update_username.html')

    def post(self, request):
        new_username = request.POST.get('new_username')
        if new_username:
            request.user.username = new_username
            request.user.save()
            return redirect('profile')  # Redirect to user's profile page after updating username
        else:
            # Handle invalid form submission
            return render(request, 'update_username.html', {'error': 'Invalid username'})

class UpdatePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm(request.user)
        return render(request, 'update_password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important for maintaining user's session
            return redirect('profile')  # Redirect to user's profile page after updating password
        else:
            # Handle invalid form submission
            return render(request, 'update_password.html', {'form': form})
        


class BookingView(PermissionRequiredMixin, View):
    permission_required = ('Website.add_booking')
    def _check_availability(boardinghouse, check_in_date, check_out_date):
        bookings = Booking.objects.filter(boarding_house=boardinghouse)
        occupied_in_date = 0
        for booking in bookings:
            if check_in_date < booking.check_out_date and check_out_date > booking.check_in_date:
                occupied_in_date += 1
        return occupied_in_date < boardinghouse.available_spaces

    def post(self, request, boardinghouse_id, *args, **kwargs):
        boardinghouse = get_object_or_404(BoardingHouse, id=boardinghouse_id)
        form = BookingForm(request.POST)

        if form.is_valid():
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']
            client_notes = form.cleaned_data['client_notes']

            # Perform any additional validation or processing here
            if check_in_date >= check_out_date:
                form.add_error('check_out_date', 'Check-out date must be later than check-in date')
                return render(request, 'boardinghouse_detail.html', {'boardinghouse': boardinghouse, 'form': form})
            if BookingView._check_availability(boardinghouse, check_in_date, check_out_date):
                # Create a Booking instance
                booking = Booking.objects.create(
                    user=request.user,
                    boarding_house=boardinghouse,
                    check_in_date=check_in_date,
                    check_out_date=check_out_date,
                    status='pending',
                    client_notes=client_notes,
                )
                booking.save()

                messages.success(request, 'Booking successful! Check your booking history for details.')
                return redirect('booking_history')
            else:
                messages.error(request, 'Booking failed! The boardinghouse is fully booked for the selected dates.')
                return render(request, 'boardinghouse_detail.html', {'boardinghouse': boardinghouse, 'form': form})

        # If form is not valid, re-render the page with the form and error messages
        return render(request, 'boardinghouse_detail.html', {'boardinghouse': boardinghouse, 'form': form})



class BookingHistoryView(PermissionRequiredMixin, View):
    permission_required = ('Website.view_booking')
    def get(self, request, *args, **kwargs):
        bookings = Booking.objects.filter(user=request.user)
        return render(request, 'booking_history.html', {'bookings': bookings})



class OwnerDashboardView(PermissionRequiredMixin, View):
    permission_required = ('Website.view_boardinghouse', 'Website.view_booking', 'Website.add_boardinghouse')

    def get(self, request, *args, **kwargs):
        user = request.user
        boarding_houses = BoardingHouse.objects.filter(user=user)
        bookings = Booking.objects.filter(boarding_house__in=boarding_houses)
        context = {'boarding_houses': boarding_houses, 'bookings': bookings}
        return render(request, 'owner_dashboard.html', context)

class UpdateBookingStatusView(PermissionRequiredMixin, View):
    permission_required = ('Website.change_booking')

    def post(self, request, booking_id, *args, **kwargs):
        print("update booking status view")
        new_status = request.POST.get('status')
        notes = request.POST.get('owner_notes')
        if new_status in dict(Booking.STATUS_CHOICES):
            booking = Booking.objects.get(id=booking_id)
            booking.status = new_status
            booking.owner_notes = notes
            booking.save()
            return redirect('owner_dashboard')
        return HttpResponseBadRequest('Invalid form submission')
class BoardinghouseListView(View):
    def get(self, request, *args, **kwargs):
        boardinghouses = BoardingHouse.objects.all()
        return render(request, 'boardinghouse_list.html', {'boardinghouses': boardinghouses})

class BoardinghouseDetailView(View):
    def get(self, request, boardinghouse_id, *args, **kwargs):
        boardinghouse = get_object_or_404(BoardingHouse, id=boardinghouse_id)
        form = BookingForm()
        return render(request, 'boardinghouse_detail.html', {'boardinghouse': boardinghouse, 'form': form})

class AddBoardinghouseView(PermissionRequiredMixin, View):
    permission_required = ('Website.add_boardinghouse')

    def get(self, request, *args, **kwargs):
        form = BoardingHouseForm()
        return render(request, 'add_boardinghouse.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = BoardingHouseForm(request.POST)
        if form.is_valid():
            boardinghouse = form.save(commit=False)
            boardinghouse.user = request.user
            boardinghouse.save()

            # Add success message
            messages.success(request, 'Boardinghouse has been successfully added.')

            return redirect('owner_dashboard')
        return render(request, 'add_boardinghouse.html', {'form': form})
    
class DeleteBoardinghouseView(PermissionRequiredMixin, View):
    permission_required = ('Website.delete_boardinghouse')
    def _update_boardinghouse_bookings(boardinghouse, status, owner_notes):
        bookings = Booking.objects.filter(boarding_house=boardinghouse)
        for booking in bookings:
            booking.status = status
            booking.owner_notes = owner_notes
            booking.save()

    def post(self, request, boardinghouse_id, *args, **kwargs):
        if (boardinghouse := BoardingHouse.objects.filter(id=boardinghouse_id, user=request.user).first() is None):
            messages.error(request, 'You are not authorized to delete this boardinghouse.')
            return redirect('owner_dashboard')
        boardinghouse = get_object_or_404(BoardingHouse, id=boardinghouse_id)
        DeleteBoardinghouseView._update_boardinghouse_bookings(boardinghouse, status='declined', owner_notes='Boardinghouse has been deleted.')
        boardinghouse.delete()
        messages.success(request, 'Boardinghouse has been successfully deleted.')
        return redirect('owner_dashboard')
    
class AddReviewView(PermissionRequiredMixin, View):
    permission_required = ('Website.add_review')

    def post(self, request, boardinghouse_id, *args, **kwargs):
        boardinghouse = get_object_or_404(BoardingHouse, id=boardinghouse_id)
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        if rating and review:
            review = Review.objects.create(
                user=request.user,
                boarding_house=boardinghouse,
                rating=rating,
                review=review,
            )
            review.save()
            messages.success(request, 'Review has been successfully added.')
            return redirect('boardinghouse_detail', boardinghouse_id=boardinghouse_id)
        return HttpResponseBadRequest('Invalid form submission')
# views.py
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import BoardingHouse, Booking, Profile, Review, Dog
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
from .forms import UpdateUsernameForm, UpdatePasswordForm, DogForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic.edit import CreateView

class HomeView(View):
    def _highest_rated_boardinghouses():
        #TODO: implement this method
        boardinghouses = BoardingHouse.objects.all()
        return boardinghouses[:2]

    def get(self, request, *args, **kwargs):
        featured_boardinghouses = HomeView._highest_rated_boardinghouses()
        return render(request, 'home.html', {'featured_boardinghouses': HomeView._highest_rated_boardinghouses()})

class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'about.html')
    
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
        dogs = Dog.objects.filter(owner=request.user)
        print("dogs:",dogs)
        return render(request, 'profile.html', {'form': form, 'profile': profile, 'dogs': dogs})

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
            if Profile.objects.filter(user__username=new_username).exists():
                return render(request, 'update_username.html', {'error': 'Username already exists'})
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
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            dog = form.cleaned_data['dog']
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
                    dog = dog,
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
                return render(request, 'boardinghouse_detail.html', {'boardinghouse': boardinghouse, 'form': form,'error':'Booking failed! The boardinghouse is fully booked for the selected dates.'})

        # If form is not valid, re-render the page with the form and error messages
        return render(request, 'boardinghouse_detail.html', {'boardinghouse': boardinghouse, 'form': form})



class BookingHistoryView(PermissionRequiredMixin, View):
    permission_required = ('Website.view_booking')
    def get(self, request, *args, **kwargs):
        bookings = Booking.objects.filter(user=request.user)
        # Get all boardinghouses that the user has reviewed
        reviwed_boardinghouses= [boardinghouse for boardinghouse in BoardingHouse.objects.all() if Review.objects.filter(user=request.user, boarding_house=boardinghouse).exists()]
        return render(request, 'booking_history.html', {'bookings': bookings, 'reviewed_boardinghouses': reviwed_boardinghouses})



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
        boardinghouses_and_avarege_reates = {}
        
        for boardinghouse in boardinghouses:
            reviews = Review.objects.filter(boarding_house=boardinghouse)
            amount_of_reviews = len(reviews)
            if reviews:
                average_rating = sum([review.rating for review in reviews]) / len(reviews)
            else:
                average_rating = 0
            boardinghouses_and_avarege_reates[boardinghouse] = (average_rating, amount_of_reviews)
        
        print(boardinghouses_and_avarege_reates)
        return render(request, 'boardinghouse_list.html', {'boardinghouses_and_rates': boardinghouses_and_avarege_reates})

class BoardinghouseDetailView(View):
    def get(self, request, boardinghouse_id, *args, **kwargs):
        boardinghouse = get_object_or_404(BoardingHouse, id=boardinghouse_id)
        if request.user.is_authenticated:
            form = BookingForm(user=request.user)
            return render(request, 'boardinghouse_detail.html', {'boardinghouse': boardinghouse, 'form': form})
        return render(request, 'boardinghouse_detail.html', {'boardinghouse': boardinghouse})

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
    def get(self, request, boardinghouse_id, *args, **kwargs):
        boardinghouse = get_object_or_404(BoardingHouse, id=boardinghouse_id)
        return render(request, 'add_review.html', {'boardinghouse': boardinghouse})
    def post(self, request, boardinghouse_id, *args, **kwargs):
        if Review.objects.filter(user=request.user, boarding_house=boardinghouse_id).exists():
            print('Review already exists')
            messages.error(request, 'You have already reviewed this boardinghouse.')
            return redirect('boardinghouse_detail', boardinghouse_id=boardinghouse_id)
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


class ReviewView(View):

    def get(self, request,boardinghouse_id,*args, **kwargs):
        boardinghouse_name = BoardingHouse.objects.get(id=boardinghouse_id).name
        user_reviews = Review.objects.filter(user=request.user, boarding_house=boardinghouse_id)
        reviews = Review.objects.filter(boarding_house=boardinghouse_id)
        return render(request, 'reviews.html', {'reviews': reviews, 'user_reviews': user_reviews, 'boardinghouse_name': boardinghouse_name})
    
    def post(self, request, review_id, *args, **kwargs):
        # check if the user has permission to delete reviews
        if not request.user.has_perm('Website.delete_review'):
            messages.error(request, 'You are not authorized to delete reviews.')
            return redirect('boardinghouse_list')
        # check if the review exists and the user is the owner of the review
        if (review := Review.objects.filter(id=review_id, user=request.user).first() is None):
            messages.error(request, 'You are not authorized to delete this review.')
            return redirect('boardinghouse_list')
        review = get_object_or_404(Review, id=review_id)
        review.delete()
        messages.success(request, 'Review has been successfully deleted.')
        return redirect('reviews', boardinghouse_id=review.boarding_house.id)
    

class AddDogView(PermissionRequiredMixin, CreateView):
    permission_required = ('Website.add_dog')
    model = Dog
    form_class = DogForm
    template_name = 'add_dog.html'
    success_url = '/user/profile/'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class DogDetailView(View):
    def get(self, request, chip_id, *args, **kwargs):
       
        dog = get_object_or_404(Dog, chip_id=chip_id)
        return render(request, 'dog_detail.html', {'dog': dog})
    def post(self, request, dog_id, *args, **kwargs):
        if (dog := Dog.objects.filter(chip_id=dog_id, owner=request.user).first() is None):
            messages.error(request, 'You are not authorized to delete this dog.')
            return redirect('profile')
        dog = get_object_or_404(Dog, chip_id=dog_id)
        dog.delete()
        messages.success(request, 'Dog has been successfully deleted.')
        return redirect('profile')

class DogUpdateView(UpdateView):
    model = Dog
    fields = ['name', 'owner', 'medicines', 'vaccination', 'age', 'gender', 'race', 'weight', 'social_level', 'walking_requirements']
    template_name = 'dog_update.html'
    def get_success_url(self):
        return reverse_lazy('dog_detail', kwargs={'chip_id': self.object.chip_id})

    def get_object(self, queryset=None):
        chip_id = self.kwargs.get('chip_id')
        return get_object_or_404(Dog, chip_id=chip_id)
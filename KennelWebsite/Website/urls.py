from django.urls import path
from .views import (
    HomeView,
    BoardinghouseListView,
    BoardinghouseDetailView,
    BookingHistoryView,
    OwnerDashboardView,
    UpdateBookingStatusView,
    AddBoardinghouseView,
    DeleteBoardinghouseView,
    BookingView,
    AddReviewView,
    ReviewView,
    AddDogView,
    DogDetailView,
    DogUpdateView,
    AboutView,
    


)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('boardinghouses/', BoardinghouseListView.as_view(), name='boardinghouse_list'),
    path('boardinghouses/<int:boardinghouse_id>/', BoardinghouseDetailView.as_view(), name='boardinghouse_detail'),
    path('boardinghouses/<int:boardinghouse_id>/delete/', DeleteBoardinghouseView.as_view(), name='delete_boardinghouse'),
    path('boardinghouses/<int:boardinghouse_id>/book', BookingView.as_view(), name='booking'),
    path('boardinghouses/add/', AddBoardinghouseView.as_view(), name='add_boardinghouse'),
    path('boardinghouses/<int:boardinghouse_id>/add-review/', AddReviewView.as_view(), name='add_review'),
    path('boardinghouses/<int:boardinghouse_id>/reviews/', ReviewView.as_view(), name='reviews'),
    path('boardinghouses/reviews/<int:review_id>/delete/', ReviewView.as_view(), name='delete_review'),
    path('booking/history/', BookingHistoryView.as_view(), name='booking_history'),
    path('owner/dashboard/', OwnerDashboardView.as_view(), name='owner_dashboard'),
    path('update-booking-status/<int:booking_id>/', UpdateBookingStatusView.as_view(), name='update_booking_status'),
    path('dogs/add-dog/', AddDogView.as_view(), name='add_dog'),
    path('dogs/<str:chip_id>/delete/', DogDetailView.as_view(), name='delete_dog'),
    path('dogs/<str:chip_id>/', DogDetailView.as_view(), name='dog_detail'),
    path('dogs/<str:chip_id>/update/', DogUpdateView.as_view(), name='update_dog'),
    path('about/', AboutView.as_view(), name='about'),
]

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


)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('boardinghouses/', BoardinghouseListView.as_view(), name='boardinghouse_list'),
    path('boardinghouses/<int:boardinghouse_id>/', BoardinghouseDetailView.as_view(), name='boardinghouse_detail'),
    path('boardinghouses/<int:boardinghouse_id>/delete/', DeleteBoardinghouseView.as_view(), name='delete_boardinghouse'),
    path('booking/history/', BookingHistoryView.as_view(), name='booking_history'),
    path('owner/dashboard/', OwnerDashboardView.as_view(), name='owner_dashboard'),
    path('update-booking-status/<int:booking_id>/', UpdateBookingStatusView.as_view(), name='update_booking_status'),
    path('boardinghouses/add/', AddBoardinghouseView.as_view(), name='add_boardinghouse'),
]

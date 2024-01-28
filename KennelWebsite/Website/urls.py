from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('boardinghouses/', views.boardinghouse_list, name='boardinghouse_list'),
    path('boardinghouses/<int:boardinghouse_id>/', views.boardinghouse_detail, name='boardinghouse_detail'),
    path('booking/history/', views.booking_history, name='booking_history'),
    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    path('boardinghouses/add/', views.add_boardinghouse, name='add_boardinghouse'),
    path('logout/', views.custom_logout, name='logout'),
    path('update-booking-status/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),

 
]

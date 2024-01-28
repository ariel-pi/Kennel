# admin.py

from django.contrib import admin
from .models import Profile, BoardingHouse, Booking

admin.site.register(Profile)
admin.site.register(BoardingHouse)
admin.site.register(Booking)

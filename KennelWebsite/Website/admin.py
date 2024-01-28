# admin.py

from django.contrib import admin
from .models import  BoardingHouse, Booking #,Profile

# admin.site.register(Profile)
admin.site.register(BoardingHouse)
admin.site.register(Booking)

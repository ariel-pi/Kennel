# admin.py

from django.contrib import admin
from .models import  BoardingHouse, Booking ,Profile, Review, Dog

admin.site.register(Profile)
admin.site.register(BoardingHouse)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Dog)

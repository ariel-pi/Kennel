# models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)

    def __str__(self):
        return self.user.username

class BoardingHouse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    contact_details = models.CharField(max_length=255)
    available_spaces = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    boarding_house = models.ForeignKey(BoardingHouse,  on_delete=models.SET_NULL, null=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    owner_notes = models.TextField(blank=True, null=True)
    client_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.boarding_house.name} ({self.status})"

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    boarding_house = models.ForeignKey(BoardingHouse, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.boarding_house.name} ({self.rating})"
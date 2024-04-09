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



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    boarding_house = models.ForeignKey(BoardingHouse, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.boarding_house.name} ({self.rating})"

class Dog(models.Model):
    chip_id = models.CharField(primary_key=True, max_length=50, unique=True, verbose_name="CHIPID")
    name = models.CharField(max_length=20, verbose_name="Dog's name")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Owner")
    medicines = models.CharField(max_length=80, verbose_name="Dog's medicines")
    VACCINATION_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No')
    ]
    vaccination = models.CharField(max_length=3, choices=VACCINATION_CHOICES, verbose_name="Vaccination", help_text="User type selection (yes/no)")
    age = models.IntegerField(verbose_name="Dog's age")
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female')
    ]
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES, verbose_name="Gender", help_text="User type selection (male/female)")
    race = models.CharField(max_length=20, verbose_name="Dog's race")
    weight = models.FloatField(verbose_name="Dog's weight")
    social_level = models.CharField(max_length=100, verbose_name="Dog's social level")
    walking_requirements = models.CharField(max_length=100, verbose_name="Dog's walking requirements")

    def __str__(self):
        return self.name+ ", id:"+self.chip_id
    
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
    dog = models.ForeignKey(Dog, on_delete=models.SET_NULL, null=True)
    

    def __str__(self):
        return f"{self.user.username} - {self.boarding_house.name} ({self.status})"

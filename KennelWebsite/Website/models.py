# models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)

    def __str__(self):
        return self.user.username

class BoardingHouse(models.Model):
    DEFAULT_MAP_LOCATION = r"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3487844.11496039!2d32.44041769453558!3d31.383867609568092!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x1500492432a7c98b%3A0x6a6b422013352cba!2sIsrael!5e0!3m2!1sen!2sil!4v1712740457423!5m2!1sen!2sil"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    map_location = models.URLField(default=DEFAULT_MAP_LOCATION, max_length=1000)
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

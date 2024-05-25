from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Booking,  BoardingHouse ,Profile, Dog
from django.contrib.auth.models import User, Group
from django import forms
from django.forms import DateInput
from django.core.exceptions import ValidationError


class BookingForm(forms.ModelForm):
    check_in_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    check_out_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['dog'].queryset = Dog.objects.filter(owner=user)

    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'client_notes', 'dog']


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["profile_picture"]


class RegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('owner', 'Boardinghouse Owner'),
    ]

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user_type = self.cleaned_data.get('user_type')

        if commit:
            user.save()
            # Assign the user to the selected group based on the user_type
            group_name = 'Boardinghouse Owners' if user_type == 'owner' else 'Customers'
            group, created = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

        return user


class UpdateUsernameForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username']

class UpdatePasswordForm(PasswordChangeForm):
    pass



class BoardingHouseForm(forms.ModelForm):
    class Meta:
        model = BoardingHouse
        fields = ['name', 'description', 'location', 'contact_details', 'available_spaces']

    def clean_contact_details(self):
        contact_details = self.cleaned_data.get('contact_details')
        # Check if contact_details is a valid phone number with 9 or 10 digits
        if not (contact_details.isdigit() and len(contact_details) in [9, 10]):
            raise ValidationError("Please enter a valid phone number with 9 or 10 digits.")
        return contact_details
    
class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = ['chip_id', 'name', 'medicines', 'vaccination', 'age','gender','race','weight','social_level','walking_requirements']
        # fields = '__all__'

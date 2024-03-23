from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Booking,  BoardingHouse ,Profile
from django.contrib.auth.models import User, Group


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'client_notes']


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

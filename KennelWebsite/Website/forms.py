from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Booking,  BoardingHouse #Profile,
from django.contrib.auth.models import User, Group

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date']


# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['first_name', 'last_name', 'phone_number', 'address']
#         # fields = ['first_name', 'last_name', 'phone_number', 'address', 'profile_picture']


#     widgets = {
#         'address': forms.Textarea(attrs={'rows': 3}),
#     }

#     # labels = {
#     #     'profile_picture': 'Profile Picture',
#     # }



class RegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('owner', 'Boardinghouse Owner'),
    ]

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

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
    
class BoardingHouseForm(forms.ModelForm):
    class Meta:
        model = BoardingHouse
        fields = ['name', 'description', 'location', 'contact_details', 'available_spaces']

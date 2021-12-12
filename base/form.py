from django.forms import ModelForm
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username',
                  'first_name', 'last_name', 'email']


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'email', 'bio']


class UserSettingsForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'first_name',
                  'last_name', 'username', 'email', 'bio']

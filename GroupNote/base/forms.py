from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Room, Note, User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class UserForm(ModelForm):
    class Meta:
        model = User 
        fields = ['username', 'email', 'name', 'avatar','bio']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"
        
        exclude = ["host", "invited", "participants"]

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note

        fields = "__all__"
        exclude = ["user", "recipients"]




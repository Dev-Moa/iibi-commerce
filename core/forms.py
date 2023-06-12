from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser,Product
from django import forms




class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('profile',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name","image","description","category","price"]

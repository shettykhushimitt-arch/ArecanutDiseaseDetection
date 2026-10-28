from django import forms
from .models import UserRegister


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = UserRegister
        fields = "__all__"
        

from .models import PredictionHistory

class ImageUploadForm(forms.ModelForm):

    class Meta:

        model=PredictionHistory

        fields=['uploaded_image']
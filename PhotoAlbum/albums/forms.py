from django import forms
from .models import Folder, Photo

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name']

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']

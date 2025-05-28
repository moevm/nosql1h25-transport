from .models import Application
from django.forms import ModelForm, TextInput, DateInput

class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ['destination_address','date_of_accomplishment']
        widgets = {
            "destination_address": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Адрес назначения'
            }),
            "date_of_accomplishment": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата выполения'
            }),
        }
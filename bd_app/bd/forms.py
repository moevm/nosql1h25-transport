from .models import Application
from django.forms import ModelForm, TextInput, DateInput, Select
from django import forms
from datetime import date

class ApplicationForm(forms.ModelForm):
    date_of_creation = forms.DateField(  
        initial=date.today,
        widget=forms.DateInput(attrs={'class': 'form-control','readonly': 'readonly'}),
    )
    class Meta:
        model = Application
        fields = ['destination_address','date_of_accomplishment', 'type_tc_id']
        widgets = {
            "destination_address": TextInput(attrs ={
                'class': 'form-control',
                'placeholder': 'Адрес назначения'
            }),
            "date_of_accomplishment": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата выполения'
            }),
            "type_tc_id": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Вид ТС'
            }),
        }
    def clean_date_of_creation(self):
        date_from_form = self.cleaned_data['date_of_creation']
        if date_from_form != date.today():
            raise forms.ValidationError("Дата создания должна быть сегодняшней.")
        return date_from_form
        
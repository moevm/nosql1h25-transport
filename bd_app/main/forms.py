from bd.models import Customer
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email", "first_name", "last_name") # Добавляем email

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control','placeholder': 'Логин' })
        self.fields['password'].widget.attrs.update({'class': 'form-control','placeholder': 'Пароль'})
        

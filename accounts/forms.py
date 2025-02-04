from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    phone_regex = RegexValidator(
        regex=r'^\d{8}$',
        message="Phone number must be 8 digits."
    )
    
    email = forms.EmailField(
        max_length=254,
        help_text="Required. Enter a valid email address.",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    phone_number = forms.CharField(
        validators=[phone_regex], 
        max_length=8,
        help_text="Enter your 8-digit phone number",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    is_patient = forms.BooleanField(
        required=False,
        help_text="Check if you are a patient",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    is_doctor = forms.BooleanField(
        required=False,
        help_text="Check if you are a doctor",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'is_patient', 'is_doctor', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

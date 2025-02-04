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
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XX XXX XXX'})
    )
    
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        help_text="Select your date of birth"
    )
    
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        help_text="Enter your full address"
    )
    
    profile_picture = forms.ImageField(
        required=False,
        help_text="Upload a profile picture (optional)",
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CustomUser
        fields = (
            'first_name', 'last_name', 'email', 'role', 'gender',
            'phone_number', 'address', 'date_of_birth', 'profile_picture',
            'password1', 'password2'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.RadioSelect(attrs={'class': 'role-radio'}),
            'gender': forms.RadioSelect(attrs={'class': 'gender-radio'})
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make required fields
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['role'].required = True
        self.fields['gender'].required = True
        self.fields['phone_number'].required = True
        self.fields['address'].required = True
        self.fields['date_of_birth'].required = True
        
        # Add help texts
        self.fields['first_name'].help_text = "Enter your first name"
        self.fields['last_name'].help_text = "Enter your last name"
        self.fields['role'].help_text = "Select your role"
        self.fields['gender'].help_text = "Select your gender"
        
        # Remove username field since we're using email
        if 'username' in self.fields:
            del self.fields['username']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user

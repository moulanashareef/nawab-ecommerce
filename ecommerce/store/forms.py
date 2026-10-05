from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Order

User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class LoginForm(forms.Form):
    username = forms.CharField(label="Username or email")
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        identifier = cleaned.get("username", "").strip()
        password = cleaned.get("password")
        if not identifier or not password:
            return cleaned
        username = identifier
        user = User.objects.filter(email__iexact=identifier).first()
        if user:
            username = user.get_username()
        self.user_cache = authenticate(self.request, username=username, password=password)
        if self.user_cache is None:
            raise forms.ValidationError("Invalid username/email or password.")
        if not self.user_cache.is_active:
            raise forms.ValidationError("This account is inactive.")
        return cleaned

    def get_user(self):
        return self.user_cache


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "email", "phone", "address", "city", "state", "postal_code"]
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        digits = "".join(ch for ch in phone if ch.isdigit())
        if len(digits) < 7 or len(digits) > 15:
            raise forms.ValidationError("Enter a valid phone number.")
        return phone

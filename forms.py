from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User

class PhoneLoginForm(AuthenticationForm):
    username = forms.CharField(label="رقم الهاتف", widget=forms.TextInput(attrs={"placeholder": "01xxxxxxxxx", "dir": "ltr"}))
    password = forms.CharField(label="كلمة المرور", strip=False, widget=forms.PasswordInput(attrs={"placeholder": "كلمة المرور"}))

class SignupForm(forms.ModelForm):
    password = forms.CharField(label="كلمة مرور قوية", widget=forms.PasswordInput, min_length=10)
    class Meta:
        model = User
        fields = ["display_name", "phone"]
        widgets = {
            "display_name": forms.TextInput(attrs={"placeholder": "اسمك بالكامل"}),
            "phone": forms.TextInput(attrs={"placeholder": "01xxxxxxxxx", "dir": "ltr"}),
        }
        labels = {"display_name": "الاسم بالكامل", "phone": "رقم الهاتف"}

    def clean_phone(self):
        phone = "".join(ch for ch in self.cleaned_data["phone"] if ch.isdigit() or ch == "+")
        if len(phone) < 10:
            raise forms.ValidationError("اكتب رقم هاتف صحيحًا.")
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("رقم الهاتف مسجل بالفعل.")
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["phone"]
        user.set_password(self.cleaned_data["password"])
        user.is_approved = False
        if commit:
            user.save()
        return user

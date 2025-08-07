from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import ScholarshipApplication
from .models import StudentProfile, User

# Registration Formclass
class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

# Login Formclass
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))

# Scholarship Application Form
class ScholarshipApplicationForm(forms.ModelForm):
    class Meta:
        model = ScholarshipApplication
        fields = [
            'full_name', 'address', 'dob', 'guardian_name', 'email', 'phone_number', 'gender',
            'school_name', 'grade_class', 'academic_score',
            'id_proof', 'photo', 'income_certificate', 'caste_certificate', 'nativity_certificate', 
            'signature', 'marklist'
        ]
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.RadioSelect(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),
        }

# profile of student
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['profile_picture', 'full_name', 'email', 'phone_number', 'dob', 'address', 'gender', 'school_name']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.RadioSelect(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),
        }
    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if not dob:
            raise forms.ValidationError("Date of Birth is required.")
        return dob
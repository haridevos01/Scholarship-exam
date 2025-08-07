from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Custom User Model
class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('school', 'school'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    


# Scholarship Application Model
class ScholarshipApplication(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    dob = models.DateField()
    guardian_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    school_name = models.CharField(max_length=200)
    grade_class = models.CharField(max_length=50)
    academic_score = models.CharField(max_length=100)

    # Uploaded Documents
    id_proof = models.FileField(upload_to='documents/id_proofs/')
    photo = models.FileField(upload_to='documents/photos/')
    income_certificate = models.FileField(upload_to='documents/income_certificates/')
    caste_certificate = models.FileField(upload_to='documents/caste_certificates/')
    nativity_certificate = models.FileField(upload_to='documents/nativity_certificates/')
    signature = models.FileField(upload_to='documents/signatures/')
    marklist = models.FileField(upload_to='documents/marklists/')

    submitted_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.school_name}"


class StudentProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    dob = models.DateField(null=True, blank=True)  # Allow null values to prevent IntegrityError
    address = models.TextField(blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    school_name = models.CharField(max_length=200, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='default_profile.jpg', blank=True, null=True)  # Profile Picture Field
    


    def __str__(self):
        return f"{self.full_name} - {self.user.username}"
    


class Payment(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    card_number = models.CharField(max_length=4)  # Store only last 4 digits
    expiry = models.CharField(max_length=7)  # Format: YYYY-MM
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[('success', 'Success'), ('failed', 'Failed')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.amount} USD - {self.status}"

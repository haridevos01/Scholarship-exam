from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from django.http import HttpResponse,JsonResponse  # Ensure these models exist
from .forms import RegisterForm, LoginForm, ScholarshipApplicationForm
from .models import ScholarshipApplication 
from .models import StudentProfile,Payment
from .forms import StudentProfileForm
from django.contrib.auth.forms import AuthenticationForm
from oro_app_admin .models import Notification
import uuid

# About Us view
def about_us(request):
    return render(request, 'about_us.html')

# Login View

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            # Redirect users based on their role
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'school':
                return redirect('school_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('home')  # Default fallback redirect

        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

# Logout View
@login_required
def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')

# Registration View

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)  
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  

            # Redirect to the appropriate dashboard based on role
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'school':
                return redirect('school_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('home')  # Default fallback

    else:
        form = RegisterForm()  

    return render(request, 'register.html', {'form': form}) 

# Student Dashboard View

def student_dashboard(request):
    if request.user.is_authenticated:
        # Retrieve scholarship applications for the logged-in user
        applications = ScholarshipApplication.objects.filter(user=request.user)
        
        # Retrieve or create the StudentProfile for the logged-in user
        profile, created = StudentProfile.objects.get_or_create(user=request.user)
    else:
        applications = ScholarshipApplication.objects.none()
        profile = None  # No profile for anonymous users
    
    return render(request, 'student_dashboard.html', {
        'applications': applications,
        'profile': profile  # Pass the profile object to the template
    })

# @login_required
# def update_profile(request):
#     return render(request, 'update_profile.html')

def application_management(request):
    if request.user.is_authenticated:
        applications = ScholarshipApplication.objects.filter(user=request.user)
    else:
        applications = ScholarshipApplication.objects.none()
    return render(request, 'application_management.html', {'applications':applications})


def student_application_view(request, pk=None):
    if not request.user.is_authenticated:
        return render(request, 'student_application_view.html', {'applications': []})

    if pk:
        # Fetch a specific application if pk is provided
        application = get_object_or_404(ScholarshipApplication, pk=pk, user=request.user)
        return render(request, 'student_application_detail.html', {'application': application})
    
    # Fetch all applications if no pk is provided
    applications = ScholarshipApplication.objects.filter(user=request.user)
    return render(request, 'student_application_view.html', {'applications': applications})

def delete_application(request):
    return HttpResponse("Delete Application Page")

def submit_application(request):
    if request.method == "POST":
        return HttpResponse("Application Submitted Successfully")
    return redirect('application_management')

def edit_application(request, pk):
    application = get_object_or_404(ScholarshipApplication, pk=pk)  # Fetch the application instance

    if request.method == "POST":
        form = ScholarshipApplicationForm(request.POST, request.FILES, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your scholarship application has been updated successfully!')
            return redirect('student_dashboard')  # Redirect to the dashboard after update
        else:
            messages.error(request, 'An error occurred. Please try again.')
    else:
        form = ScholarshipApplicationForm(instance=application)

    return render(request, 'edit_application.html',{'form':form})
# Payment Page


def payment(request):
    return render(request, 'payment.html')

# Apply for Scholarship
def apply_scholarship(request):
    if request.method == "POST":
        form = ScholarshipApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user  # Assign the logged-in user
            application.save()
            return redirect('student_dashboard')
    else:
        form = ScholarshipApplicationForm()
    
    return render(request, 'apply.html',{'form':form})

#student profile
# @login_required
def student_profile_view(request):
    """View student profile."""
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if user is not authenticated
    
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    return render(request, 'student_profile.html', {'profile': profile})
# @login_required
def update_profile(request):
    """Update student profile details, including profile picture."""
    profile, created = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)  # Handle file uploads
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('student_profile')
        else:
            messages.error(request, 'An error occurred. Please check your input.')
    else:
        form = StudentProfileForm(instance=profile)

    return render(request, 'update_profile.html', {'form': form})

# Exam Result Page
def exam_result(request):
    return render(request, 'exam_result.html')

# def student_profile(request):
#     return render(request, 'student_profile.html')

def download_study_material(request):
    return render(request, 'download_study_material.html')

def exam_page(request):
    return render(request, 'exam_page.html')

def faq_page(request):
    return render(request, 'faq.html')

def hall_ticket_view(request):
    return render(request, 'hall_ticket.html')


def student_notification(request):
    notifications = Notification.objects.all().order_by('-created_at')[:50]  # Fetch latest 5 notifications
    notification_count = Notification.objects.count()  # Count total notifications
    return render(request, 'student_notification.html', {'notifications': notifications,'notification_count': notification_count})


def process_payment(request):
    """Processes the payment and ensures users can only pay once."""
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        amount = request.POST.get("amount")
        card_number = request.POST.get("card")
        expiry = request.POST.get("expiry")
        cvv = request.POST.get("cvv")

        # Check if the user has already paid
        if Payment.objects.filter(name=name).exists():
            messages.error(request, "You have already completed the payment.")
            return redirect("payment")  # Redirect to monitoring page

        # Validate required fields
        if not (name and email and amount and card_number and expiry and cvv):
            messages.error(request, "All fields are required!")
            return redirect("process_payment")

        # Simulate a fake transaction ID (since there's no real payment gateway)
        transaction_id = str(uuid.uuid4())[:10]  
        status = "success"  # Always successful in demo mode

        # Save the payment in the database
        Payment.objects.create(
            name=name,
            email=email,
            amount=amount,
            card_number=card_number[-4:],  # Save only last 4 digits for security
            expiry=expiry,
            transaction_id=transaction_id,
            status=status
        )

        messages.success(request, "Payment successful!")
        return redirect("payment_status", transaction_id=transaction_id)

    return JsonResponse({"success": False, "message": "Invalid request"})


def payment_status(request, transaction_id):
    """Displays the payment status page."""
    payment = Payment.objects.filter(transaction_id=transaction_id).first()
    if payment:
        return render(request, "process_payment.html", {"payment": payment})
    else:
        return render(request, "process_payment.html", {"error": "Transaction not found!"})

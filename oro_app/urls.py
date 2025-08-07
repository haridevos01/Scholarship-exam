from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about_us, name='about_us'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('application_management/', views.application_management, name='application_management'),
    path('application/delete/', views.delete_application, name='delete_application'),
    path('application/submit/', views.submit_application, name='submit_application'),
    path('payment/', views.payment, name='payment'),
    path('apply/', views.apply_scholarship, name='apply_scholarship'),
    path('exam_result/', views.exam_result, name='exam_result'),
    path('application/edit/<int:pk>/', views.edit_application, name='edit_application'),
    path('application_view/<int:pk>/', views.student_application_view, name='student_application_view'),
    path('student_profile/', views.student_profile_view, name='student_profile'),
    path('download_study_material/', views.download_study_material, name='download_study_material'),
    path('exam/', views.exam_page, name='exam_page'),
    path('faq/', views.faq_page, name='faq_page'),
    path('hall_ticket/', views.hall_ticket_view, name='hall_ticket'),
    path('student_notification/',views.student_notification,name='student_notification'),
    path('process_payment/',views.process_payment,name='process_payment'),
    path('payment_status/<str:transaction_id>/',views.payment_status,name='payment_status'),
]
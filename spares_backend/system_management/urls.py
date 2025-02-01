from django.urls import path

from system_management import views


urlpatterns = [

    # User
    path('sign_up/', views.sign_up, name = 'sign_up'),
    path('user_login/', views.user_login, name = 'user_login'),
    path('user_logout/', views.user_logout, name = 'user_logout'),
    path('reset_password/', views.reset_password, name = 'reset_password'),
    path('forgot_password/', views.forgot_password, name = 'forgot_password'),
    path('change_password/', views.change_password, name = 'change_password'),

    # Profile
    path('edit_profile/', views.edit_profile, name = 'edit_profile'),
    path('view_profile/', views.view_profile, name = 'view_profile'),
    path('create_profile/', views.create_profile, name = 'create_profile'),

    # OTP
    path('send_otp/', views.send_otp, name = 'send_otp'),
    path('create_otp/', views.create_otp, name = 'create_otp'),
    path('resend_otp/', views.resend_otp, name = 'resend_otp'),
    path('verify_otp/', views.verify_otp, name = 'verify_otp'),

    # Add user
    path('edit_user/', views.edit_user, name = 'edit_user'),
    path('view_users/', views.view_users, name = 'view_users'),
    path('view_admin/', views.view_admin, name = 'view_admin'),
    path('create_user/', views.create_user, name = 'create_user'),
    path('view_customer/', views.view_customer, name = 'view_customer'),
    
]
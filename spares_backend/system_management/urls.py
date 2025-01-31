from django.urls import path

from system_management import views


urlpatterns = [
    path('sign_up/', views.sign_up, name = 'sign_up'),
    path('user_login/', views.user_login, name = 'user_login'),
    path('edit_profile/', views.edit_profile, name = 'edit_profile'),
    path('create_profile/', views.create_profile, name = 'create_profile'),

]
from django.urls import path

from product_management import views


urlpatterns = [

    # Categoty
    path('edit_category/', views.edit_category, name = 'edit_category'),
    path('view_category/', views.view_category, name = 'view_category'),
    path('create_category/', views.create_category, name = 'create_category'),
    path('view_categories/', views.view_categories, name = 'view_categories'),
    path('view_categoty_profile/', views.view_categoty_profile, name = 'view_categoty_profile'),

    # Product
    path('edit_product/', views.edit_product, name = 'edit_product'),
    path('view_product/', views.view_product, name = 'view_product'),
    path('view_products/', views.view_products, name = 'view_products'),
    path('create_product/', views.create_product, name = 'create_product'),
]
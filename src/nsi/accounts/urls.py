from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.account_page, name='account'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('new/', views.create_page, name='new-account'),
    path('delete/', views.delete_page, name='delete-account'),
    path('new-password/', views.new_password_page, name='new-password-account'),
    path('forgot-password/', views.forgot_password_page, name='forgot-password-account'),
]
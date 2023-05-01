from django.urls import path
from app import views

urlpatterns = [
    path('', views.app_page, name='app-index'),
    path('edit/<str:url>', views.edit_page, name='edit-url'),
    path('delete/<str:url>', views.delete_page, name='delete-url'),
    path('add', views.add_page, name='add-url'),
]

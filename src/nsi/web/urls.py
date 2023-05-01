from django.urls import path
from web import views

urlpatterns = [
    path('', views.index_page, name='index'),
    path('sitemap', views.sitemap_page, name='sitemap'),
    path('contact/', views.contact_page, name='contact'),
    path('cgu/', views.cgu_page, name='cgu'),
    path('a-propos/', views.a_propos_page, name='a-propos'),
    path('<str:key>', views.url_page, name='url'),
]

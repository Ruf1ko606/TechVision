from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services_view, name='services'),
    # ВОТ ЭТОТ МАРШРУТ ОН ИЩЕТ: Убедись, что он здесь и name='service_detail'
    path('services/<slug:slug>/', views.service_detail_view, name='service_detail'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('user-agreement/', views.user_agreement, name='user_agreement'),
    path('about/', views.about_view, name='about'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('portfolio/', views.portfolio_view, name='portfolio'), 
    path('portfolio/<slug:slug>/', views.project_detail_view, name='project_detail'),
]


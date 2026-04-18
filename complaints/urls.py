from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('complaints/', views.complaint_list, name='complaint_list'),
    path('complaints/create/', views.complaint_create, name='complaint_create'),
    path('complaints/<int:pk>/', views.complaint_detail, name='complaint_detail'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='user_logout'),
]

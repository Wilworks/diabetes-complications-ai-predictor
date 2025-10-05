"""
URL configuration for predictor app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('predict/', views.predict, name='predict'),
    path('results/<int:prediction_id>/', views.results, name='results'),
]
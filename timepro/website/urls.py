from django.urls import path

from website import views


urlpatterns = [
    path('register/', views.register),
]
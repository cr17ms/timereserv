from django.urls import path
from django.views.i18n import JavaScriptCatalog

from website import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('home/', views.home, name='home'),
    path('addtime/', views.addtime, name='addtime'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
]

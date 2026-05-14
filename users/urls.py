from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView  # Importe a nova view

app_name = 'users'

urlpatterns = [
    # Use a CustomLoginView em vez da padrão
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('recover/', views.recover, name='recover'),
]
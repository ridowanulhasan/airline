from django.urls import path
from . import views

urlpatterns = [
    # Define your user-related URL patterns here
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
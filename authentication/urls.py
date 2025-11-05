from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('change_password/',views.changePasswordView.as_view(),name='change_password'),
    path('new_password/',views.NewPasswordView.as_view(),name='new_password')
]
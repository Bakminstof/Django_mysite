from django.urls import path

from app_users.views import (
    LoginView,
    LogoutView,
    RegisterView,
    AccountView,
    CardView
)

app_name = 'app_users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('account/', AccountView.as_view(), name='account'),
    path('card/', CardView.as_view(), name='card'),
]

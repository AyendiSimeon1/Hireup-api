from django.urls import path
from .views import RegisterView, LoginView, Profile


urlpatterns= [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', Profile.as_view(), name='profile'),

]
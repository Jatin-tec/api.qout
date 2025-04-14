from django.urls import path
import users.api.views as user_views
from users.api.views import RegisterView, ProfileView

urlpatterns = [
    path('login/', user_views.LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
]

from django.urls import path
import users.api.views as user_views

urlpatterns = [
    path('login/', user_views.LoginView.as_view(), name='login'),
    # path('register/', user_views),
]

from django.contrib.auth import views
from django.urls import path

from .forms import UserLoginForm
from .views import signup

# Create your views here.
urlpatterns = [
    path('login/', views.LoginView.as_view(template_name='login.html', authentication_form=UserLoginForm),
         name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path('home/', login_required(TemplateView.as_view(template_name='home.html')), name='home'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("ganaderia/", include("ganaderia.urls"), name="home_g"),
]

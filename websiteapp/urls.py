
from django.contrib import admin
from django.urls import path
from account import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path("login", views.loginView, name = "login"),
    path("logout",views.logoutView,name="logout"),
    path("register",views.registerView, name ="register"),
    path("", views.homeView,name ="home"),
    path('admin/', admin.site.urls),
    path("password", views.change_password, name = "change_password"),
    path("successL", TemplateView.as_view(template_name="successL.html"),name = "successL"),
    path("successR", TemplateView.as_view(template_name="successR.html"), name="successR"),
    path("successP", TemplateView.as_view(template_name="successP.html"), name="successP")
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload, name='upload'),
    path('download/', views.download, name='download'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path("download/<str:encrypted_id>/", views.download_file, name="download_file"),
    path("files/", views.file_list, name="file_list"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),


]

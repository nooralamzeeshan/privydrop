from django.contrib import admin
from django.urls import path
from app_django import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('upload/', views.upload, name='upload'),
    path('download/', views.download, name='download'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('files/', views.file_list, name='file_list'),
    path('files/<str:encrypted_id>/', views.download_file, name='download_file'),
]

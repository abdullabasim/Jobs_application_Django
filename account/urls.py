from django.urls import path,include
from . import views


urlpatterns = [
    path('register/', views.register,name='register'),
    path('me/', views.currentUser,name='get-current-user'),
    path('me/update', views.updateUser, name='update-user'),
    path('upload/resume', views.uploadResume, name='upload-resume'),
]
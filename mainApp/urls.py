from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('upload/', UploadFile.as_view(), name='upload'),
    path('', ViewSaves.as_view(), name='view-saves'),
    path('create-save/', CreateSave.as_view(), name='create-save')
]

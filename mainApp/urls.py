
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
	path('save/<int:pk>/upload/', UploadFile.as_view(), name='upload'),
	path('', ViewSaves.as_view(), name='view-saves'),
	path('create-save/', CreateSave.as_view(), name='create-save'),
	path('save/<int:pk>', SaveView.as_view(), name='save-page'),
	path('save/<int:pk>/delete', DeleteSave.as_view(), name='delete-save'),
	path('save/<int:pk>/<str:name>', PlayerView.as_view(), name='player-page'),
	path('save/<int:pk>/season/<int:pk2>', SeasonView.as_view(), name='season-page'),
	path('save/<int:pk>/season/<int:pk2>/delete', DeleteSeason.as_view(), name='delete-season'),
	path('save/<int:pk>/season/<int:pk2>/edit', EditSeason.as_view(), name='edit-season')
]

from django.urls import path
from drive import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('callback/', views.callback, name='callback'),
    path('list/', views.list_files, name='list_files'),
    path('upload/', views.upload_file, name='upload_file'),
    path('download/<str:file_id>/', views.download_file, name='download_file'),
    path('delete/<str:file_id>/', views.delete_file, name='delete_file'),
]

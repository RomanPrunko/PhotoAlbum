from django.urls import path
from . import views

urlpatterns = [
    path('', views.album_list, name='album_list'),
    path('folder/<int:folder_id>/', views.album_detail, name='album_detail'),
    path('folder/<int:parent_id>/create/', views.create_folder, name='create_subfolder'),
    path('create-root-folder/', views.create_folder, name='create_folder'),  # коренева папка
    path('folder/<int:folder_id>/edit/', views.edit_folder, name='edit_folder'),
    path('folder/<int:folder_id>/delete/', views.delete_folder, name='delete_folder'),
    path('folder/<int:folder_id>/upload/', views.upload_photo, name='upload_photo_in_folder'),
    path('upload/', views.upload_photo, name='upload_photo'),
    path('photo/<int:photo_id>/confirm_delete/', views.photo_delete_confirm, name='photo_delete_confirm'),
]

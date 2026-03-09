from django.urls import path
from . import views


urlpatterns = [
    path('<int:category_id>/', views.posts_by_category, name='posts_by_category'),
    path('delete-comment/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('edit-comment/<int:pk>/', views.edit_comment, name='edit_comment'),
]
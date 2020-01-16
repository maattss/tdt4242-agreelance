from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('new/', views.new_project, name='new_project'),
    path('<project_id>/', views.project_view, name='project_view'),
    path('<project_id>/tasks/<task_id>/', views.task_view, name='task_view'),
    path('<project_id>/tasks/<task_id>/upload/', views.upload_file_to_task, name='upload_file_to_task'),
    path('<project_id>/tasks/<task_id>/permissions/', views.task_permissions, name='task_permissions'),
    path('delete_file/<file_id>', views.delete_file, name='delete_file'),
]

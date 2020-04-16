from django.urls import path
from projects.views import new_project, project_view, task_view, delete_file

urlpatterns = [
    path('', project_view.projects_all, name='projects_all'),
    path('new/', new_project.new_project, name='new_project'),
    path('all/', project_view.projects_all, name='projects_all'),
    path('all/<category_id>', project_view.projects, name='projects'),
    path('all/<category_id>/<tag_name>', project_view.projects_tags, name='projects_tags'),
    path('<project_id>/', project_view.project_view, name='project_view'),
    path('<project_id>/tasks/<task_id>/', task_view.task_view, name='task_view'),
    path('<project_id>/tasks/<task_id>/upload/', task_view.upload_file_to_task, name='upload_file_to_task'),
    path('<project_id>/tasks/<task_id>/permissions/', task_view.task_permissions, name='task_permissions'),
    path('delete_file/<file_id>', delete_file.delete_file, name='delete_file'),
]

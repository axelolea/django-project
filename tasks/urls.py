from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks/<int:task_id>', views.detail_task, name='task_detail'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/edit/<int:task_id>', views.edit_task, name='edit_task'),
    path('tasks/complete/<int:task_id>', views.complete_task, name='complete_task'),
    path('tasks/delete/<int:task_id>', views.delete_task, name='delete_task'),
    path('signup/', views.signup, name='signup'),
    path('logout', views.logout_user, name='logout'),
    path('login', views.login_user, name='login'),
]
from django.urls import path
from . import views
app_name = 'tasks'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('detail/<int:task_id>', views.detail, name='detail'),
    path('edit/<int:task_id>', views.edit, name='edit'),
    path('delete/<int:task_id>', views.delete, name='delete'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('task_list/', views.task_list, name='task_list'),
    path('user_details/', views.user_details, name='user_details'),
]

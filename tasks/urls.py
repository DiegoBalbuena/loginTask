from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'tasks'

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create, name='create'),
    path('detail/<int:task_id>', views.detail, name='detail'),
    path('edit/<int:task_id>', views.edit, name='edit'),
    path('delete/<int:task_id>', views.delete, name='delete'),
    path('login/', views.login_view, name='login'),  # Deja solo una ruta para 'login'
    path('register/', views.register_view, name='register'),  # Deja solo una ruta para 'register'
    path('task_list/', views.task_list, name='task_list'),
    path('user_details/', views.user_details, name='user_details'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('change_password/', views.change_password, name='change_password'),
    path('delete_account/', views.delete_account, name='delete_account'),
]

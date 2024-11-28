from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import TaskCreationForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout

# Vista para eliminar cuenta (requiere estar logueado)
@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        logout(request)  # Cierra la sesión tras eliminar la cuenta
        return redirect('tasks:login')  # Redirige a la página de login
    return render(request, 'delete_account.html')


# Vista para editar el usuario (requiere estar logueado)
@login_required
def edit_account(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('tasks:user_details')  # Redirige a los detalles del usuario después de editar
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'edit_account.html', {'form': form})
    
# Vista para cambiar la contrasena (requiere estar logueado)
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantener al usuario logueado después de cambiar la contraseña
            return redirect('tasks:user_details')  # Redirige a los detalles del usuario
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'change_password.html', {'form': form})
    
# Vista para la lista de tareas (requiere estar logueado)
@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

# Vista para los detalles del usuario
@login_required
def user_details(request):
    return render(request, 'user_details.html', {'user': request.user})

def index(request):
    tasks = Task.objects.all()
    params = {
        'tasks': tasks,
    }
    return render(request, 'tasks/index.html', params)


def create(request):
    if (request.method == 'POST'):
        title = request.POST['title']
        description = request.POST['description']
        task = Task(title=title, description=description)
        task.save()
        return redirect('tasks:index')
    else:
        params = {
            'form': TaskCreationForm(),
        }
        return render(request, 'tasks/create.html', params)


def detail(request, task_id):
    task = Task.objects.get(id=task_id)
    params = {
        'task': task,
    }
    return render(request, 'tasks/detail.html', params)


def edit(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        form = TaskCreationForm(request.POST)
        if form.is_valid():
            # Si el formulario es válido, actualizamos la tarea
            task.title = form.cleaned_data['title']
            task.description = form.cleaned_data['description']
            task.save()
            return redirect('tasks:detail', task_id)
    else:
        # En la solicitud GET, prellenamos el formulario con los datos existentes
        form = TaskCreationForm(initial={
            'title': task.title,
            'description': task.description,
        })
    
    return render(request, 'tasks/edit.html', {'form': form, 'task': task})



def delete(request, task_id):
    task = Task.objects.get(id=task_id)
    if (request.method == 'POST'):
        task.delete()
        return redirect('tasks:index')
    else:
        params = {
            'task': task,
        }
        return render(request, 'tasks/delete.html', params)
        

# Vista para el registro de usuario
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tasks:task_list')
        else:
            return render(request, 'register.html', {'form': form, 'errors': form.errors})
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    error = None
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('tasks:task_list')
        else:
            return render(request, 'login.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'login.html')

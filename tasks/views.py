from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    """Create a new http page for django

    Args:
        request (class): Send for page request http

    Returns:
        render: render de page for home
    """
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm,
        })
    elif request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            # Register the user
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'User has already been created',
                })

        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Password does not match',
            })
    else:
        print('Problema en Signup')

@login_required
def tasks(request):
    tasks_complete = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    tasks_incomplete = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks/tasks.html', {
        'tasks_complete': tasks_complete,
        'tasks_incomplete': tasks_incomplete,
    })


@login_required
def detail_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'tasks/task_detail.html', {
        'task': task,
    })


@login_required
def edit_task(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'tasks/task_edit.html', {
            'form': form,
            'task': task,
        })
    elif request.method == 'POST':
        try:
            task = get_object_or_404(Task, id=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks/task_edit.html', {
                'form': form,
                'task': task,
                'error': 'Error saving update task'
            })



@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'tasks/create_task.html', {
            'form': TaskForm,
        })
    elif request.method == 'POST':
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tasks/create_task.html', {
                'form': TaskForm,
                'error': 'Ingresar datos validos'
            })


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def logout_user(request):
    logout(request)
    return redirect('home')


def login_user(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm,
        })
    elif request.method == 'POST':
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'],
                            )
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'Invalid username or password'
            })
        else:
            login(request, user)
            return redirect('home')

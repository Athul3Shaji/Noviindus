from django.shortcuts import render
from django.template.context_processors import request

# Create your views here.

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import logout
from django.shortcuts import redirect

  # Replace 'login' with your actual login view name


from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from .models import Task
from .models import CustomUser
from .forms import UserCreateForm,UserUpdateForm
from django.contrib import messages



def custom_login_view(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:  # Ensure both fields are provided
            user = authenticate(
                request,
                username=username,
                password=password
            )
            if user:
                login(request, user)
                if user.role == 'superadmin':
                    return redirect('/superadmin/dashboard/')
                elif user.role == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_dashboard')
            else:
                error = "Invalid username or password"
        else:
            error = "Please enter both username and password"

    return render(request, 'login.html', {'error': error})






def logout_view(request):
    logout(request)
    return redirect('login')  # Replace 'login' with your actual login view name



@login_required
def superadmin_dashboard(request):
    if request.user.role != 'superadmin':
        raise Http404("You are not authorized to view this page.")

    # Get all users, admins, and tasks
    users = CustomUser.objects.all()
    admins = CustomUser.objects.filter(role='admin')
    tasks = Task.objects.all()

    return render(request, 'superadmin_dashboard.html', {
        'users': users,
        'admins': admins,
        'tasks': tasks,
    })


@login_required
def create_user(request):
    if request.user.role != 'superadmin':
        raise Http404("You are not authorized to perform this action.")

    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully')
            return redirect('superadmin_dashboard')
    else:
        form = UserCreateForm()

    return render(request, 'create_user.html', {'form': form})

 # View to Update a User
@login_required
def update_user(request, user_id):
    if request.user.role != 'superadmin':
        raise Http404("You are not authorized to perform this action.")

    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully')
            return redirect('superadmin_dashboard')
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'update_user.html', {'form': form, 'user': user})

# View to Delete a User
@login_required
def delete_user(request, user_id):
    if request.user.role != 'superadmin':
        raise Http404("You are not authorized to perform this action.")

    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully')
    return redirect('superadmin_dashboard')

# View to Assign Role to User
@login_required
def assign_role(request, user_id):
    if request.user.role != 'superadmin':
        raise Http404("You are not authorized to perform this action.")

    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        role = request.POST.get('role')
        user.role = role
        user.save()
        messages.success(request, f'User role updated to {role}')
        return redirect('superadmin_dashboard')

    return render(request, 'assign_role.html', {'user': user})




# View to Create a New Task
@login_required
def create_task(request):
    if request.user.role != 'superadmin':
        raise Http404("You are not authorized to perform this action.")

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        assigned_to = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')

        # Create a task
        Task.objects.create(
            title=title,
            description=description,
            assigned_to=CustomUser.objects.get(id=assigned_to),
            due_date=due_date,
            status='pending',
        )

        messages.success(request, 'Task created successfully')
        return redirect('superadmin_dashboard')

    users = CustomUser.objects.all()
    return render(request, 'create_task.html', {'users': users})

# View to Update a Task
@login_required
def update_task(request, task_id):
    if request.user.role != 'superadmin':
        raise Http404("You are not authorized to perform this action.")

    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        # Retrieve form data
        title = request.POST.get('task_title')
        description = request.POST.get('task_description')
        due_date = request.POST.get('due_date')
        status = request.POST.get('status')

        # Check if required fields are provided
        if not title or not description or not due_date or not status:
            messages.error(request, "All fields are required.")
            return render(request, 'update_task.html', {'task': task})

        # Update task with the form data
        task.title = title
        task.description = description
        task.due_date = due_date
        task.status = status

        # Save the updated task
        try:
            task.save()
            messages.success(request, 'Task updated successfully.')
            return redirect('superadmin_dashboard')
        except Exception as e:
            messages.error(request, f"Error updating task: {e}")
            return render(request, 'update_task.html', {'task': task})

    return render(request, 'update_task.html', {'task': task})
# View to Delete a Task
@login_required
def delete_task(request, task_id):
    if request.user.role != 'superadmin':
        raise Http404("You are not authorized to perform this action.")

    task = get_object_or_404(Task, id=task_id)
    task.delete()

    messages.success(request, 'Task deleted successfully')
    return redirect('superadmin_dashboard')


@login_required
def admin_dashboard(request):
    print(request.user)
    if request.user.role != 'admin':
        raise Http404("You are not authorized to view this page.")

    # tasks = Task.objects.filter(assigned_to =  request.user)
    tasks = Task.objects.all()


    return render(request, 'admin_dashboard.html', {
        'tasks': tasks,
    })


@login_required
def admin_create_task(request):
    if request.user.role != 'admin':
        raise Http404("You are not authorized to perform this action.")

    if request.method == 'POST':
        # Assuming 'task_title' and 'task_description' are coming from the form
        assigned_user_id = request.POST.get('assigned_to')
        assigned_user = CustomUser.objects.get(id=assigned_user_id)

        # Ensure the assigned user has the 'user' role
        if assigned_user.role != 'user':
            raise Http404("The selected user is not eligible for this task.")

        task = Task.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            assigned_to=assigned_user,
            # You would get this from form input (e.g., a select box for users under this admin)
            due_date=request.POST['due_date'],
            status='Pending',
        )
        task.save()
        return redirect('admin_dashboard')  # Redirect to the admin dashboard after task creation
    available_users = CustomUser.objects.filter(role='user')

    return render(request, 'admin_create_task.html', {
        'available_users': available_users  # Pass available users to the template
    })



@login_required
def admin_update_task(request, task_id):
    if request.user.role != 'admin':
        raise Http404("You are not authorized to perform this action.")

    task = get_object_or_404(Task, id=task_id)

    # Only allow updating tasks assigned to users with role 'user'
    if task.assigned_to.role != 'user':
        raise Http404("You are not authorized to update this task.")

    if request.method == 'POST':
        task.title = request.POST['task_title']
        task.description = request.POST['task_description']
        task.due_date = request.POST['due_date']
        task.status = request.POST['status']
        task.save()
        return redirect('admin_dashboard')

    return render(request, 'admin_update_task.html', {
        'task': task
    })



@login_required
def admin_delete_task(request, task_id):
    if request.user.role != 'admin':
        raise Http404("You are not authorized to perform this action.")

    task = get_object_or_404(Task, id=task_id)

    # Only allow deleting tasks assigned to users with role 'user'
    if task.assigned_to.role != 'user':
        raise Http404("You are not authorized to delete this task.")

    if request.method == 'POST':
        task.delete()
        return redirect('admin_dashboard')

    return render(request, 'admin_confirm_delete.html', {
        'task': task
    })



@login_required
def user_dashboard(request):
    if request.user.role != 'user':
        raise Http404("Unauthorized access.")

    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'user_dashboard.html', {'tasks': tasks})



@login_required
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)

    if request.method == 'POST':
        task.status = request.POST.get('status')
        task.completion_report = request.POST.get('completion_report')
        task.worked_hours = request.POST.get('worked_hours')
        task.save()
        return redirect('user_dashboard')

    return render(request, 'user_update_task.html', {'task': task})


@login_required
def view_task_report(request, task_id):
    # Fetch the task by ID
    task = get_object_or_404(Task, id=task_id)

    # Check if the current user is an admin and is allowed to view the task
    # if request.user.role == 'admin':
    #     if task.assigned_to != request.user:
    #         # If the task is not assigned to the admin, raise a 404 error
    #         raise Http404("You are not authorized to view this report.")

    # For SuperAdmin, they can view any task report
    if request.user.role == 'superadmin':
        pass

    # Render the report template with task details
    return render(request, 'view_report.html', {
        'task': task,
    })
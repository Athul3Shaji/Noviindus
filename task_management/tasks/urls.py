from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (

    custom_login_view,
    logout_view,
    superadmin_dashboard,
    create_user,
    update_user,
    delete_user,
    assign_role,
    create_task,
    update_task,
    delete_task,
    admin_dashboard,
    admin_create_task,
    admin_update_task,
    admin_delete_task,
    user_dashboard,
    update_task_status,
view_task_report
)

urlpatterns = [
    # Auth endpoints
    path('user_login/', custom_login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # SuperAdmin endpoints
    path('superadmin/dashboard/', superadmin_dashboard, name='superadmin_dashboard'),
    path('superadmin/create-user/', create_user, name='create_user'),
    path('superadmin/update-user/<int:user_id>/', update_user, name='update_user'),
    path('superadmin/delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('superadmin/assign-role/<int:user_id>/', assign_role, name='assign_role'),
    path('superadmin/create-task/', create_task, name='create_task'),
    path('superadmin/update-task/<int:task_id>/', update_task, name='update_task'),
    path('superadmin/delete-task/<int:task_id>/', delete_task, name='delete_task'),

    # Admin endpoints
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/create-task/', admin_create_task, name='admin_create_task'),
    path('dashboard/admin/update-task/<int:task_id>/', admin_update_task, name='admin_update_task'),
    path('dashboard/admin/delete-task/<int:task_id>/', admin_delete_task, name='admin_delete_task'),

    # User endpoint
    path('user/dashboard/', user_dashboard, name='user_dashboard'),
    path('user/update-task/<int:task_id>/', update_task_status, name='user_update_task'),

    path('view-report/<int:task_id>/', view_task_report, name='view_task_report'),

]

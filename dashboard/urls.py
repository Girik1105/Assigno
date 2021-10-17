from django.urls import path

from . import views 

app_name = 'dashboard'

urlpatterns = [
    path('user/profile/', views.profile_edit_view, name='edit-user-profile'),
    path('dashboard/', views.home, name='home'),
    
    path('dashboard/assignment/create/', views.create_assignments.as_view() , name='assignment-create'),
    path('dashboard/assignment/update/<pk>/', views.update_assignments.as_view() , name='assignment-update'),
    path('dashboard/assignment/list/', views.list_assignments.as_view() , name='assignment-list'),
    path('dashboard/assignment/delete/<pk>/', views.delete_assignment.as_view() , name='assignment-delete'),

    path('dashboard/category/create/', views.create_categories.as_view() , name='category-create'),
    path('dashboard/category/edit/', views.list_categories.as_view() , name='category-edit'),
    path('dashboard/category/delete/<pk>/', views.delete_categories, name='category-delete'),

    path('dashboard/notes/create/', views.create_notes.as_view() , name='notes-create'),
    path('dashboard/notes/list/', views.list_notes.as_view() , name='notes-list'),
    path('dashboard/notes/detail/<pk>/', views.detail_notes.as_view() , name='notes-detail'),
    path('dashboard/notes/delete/<pk>/', views.delete_notes.as_view() , name='notes-delete'),
    path('dashboard/notes/update/<pk>/', views.update_notes.as_view() , name='notes-update'),

    path('dashboard/reminders/add/', views.create_deadlines.as_view() , name='reminders-create'),
    path('dashboard/reminders/list/', views.list_deadlines.as_view() , name='reminders-list'),
    path('dashboard/reminders/update/<pk>/', views.update_deadlines.as_view() , name='reminders-update'),    
    path('dashboard/reminders/delete/<pk>/', views.delete_deadlines.as_view() , name='reminders-delete'),

    path('dashboard/tasks/create/', views.TaskCreate.as_view(), name='task-create'),
    path('dashboard/tasks/all/', views.TaskList.as_view(), name='task-list'),
    path('dashboard/tasks/update/<int:pk>/', views.TaskUpdate.as_view(), name='task-update'),
    path('dashboard/tasks/delete/<int:pk>/', views.TaskDelete.as_view(), name='task-delete'),

    path('meditation/', views.meditation.as_view(), name='meditation')
]
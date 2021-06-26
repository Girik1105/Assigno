from django.urls import path

from . import views 

app_name = 'dashboard'

urlpatterns = [
    path('dashboard/', views.home, name='home'),
    
    path('dashboard/assignment/create/', views.create_assignments.as_view() , name='assignment-create'),
    path('dashboard/assignment/update/<pk>/', views.update_assignments.as_view() , name='assignment-update'),
    path('dashboard/assignment/list/', views.list_assignments.as_view() , name='assignment-list'),
    path('dashboard/assignment/delete/<pk>/', views.delete_assignment.as_view() , name='assignment-delete'),

    # path('dashboard/category/create/', views.create_categories.as_view() , name='category-create'),
    # path('dashboard/category/delete/<pk>/', views.delete_categories.as_view() , name='category-delete'),

    path('dashboard/notes/create/', views.create_notes.as_view() , name='notes-create'),
    path('dashboard/notes/list/', views.list_notes.as_view() , name='notes-list'),
]
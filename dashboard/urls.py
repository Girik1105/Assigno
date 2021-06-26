from django.urls import path

from . import views 

app_name = 'dashboard'

urlpatterns = [
    path('dashboard/', views.home, name='home'),
    path('dashboard/assignment/create/', views.create_assignments.as_view() , name='assignment-create'),
    path('dashboard/assignment/list/', views.list_assignments.as_view() , name='assignment-list'),
]
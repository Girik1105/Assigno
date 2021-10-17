from django.urls import path

from . import views 

app_name = 'forums'

urlpatterns = [
    path('create/', views.create_forum.as_view(), name='create-forum'),
    path('all/', views.list_forum.as_view(), name='list-forums'),
    path('<str:slug>/', views.detail_forum.as_view(), name='detail-forum'),
]

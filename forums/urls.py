from django.urls import path

from . import views 

app_name = 'forums'

urlpatterns = [
    path('create/', views.create_forum.as_view(), name='create-forum'),
    path('all/', views.list_forum.as_view(), name='list-forums'),
    path('<str:slug>/', views.detail_forum.as_view(), name='detail-forum'),
    path('update/<str:slug>/', views.update_forum.as_view(), name='update-forum'),

    path("join/<str:slug>/",views.join_forum.as_view(),name="join-forum"),
    path("leave/<str:slug>/",views.leave_forum.as_view(),name="leave-forum"),
]

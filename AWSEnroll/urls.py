from django.urls import path
from django.http import HttpResponse
from django.contrib.auth.views import LogoutView
from .views import (ProjectView, ProjectCreate, UserUpdate, ProjectList, 
    ProjectDelete, ProjectMemberList, CustomLoginview)

urlpatterns = [
    path('', ProjectView.as_view(), name='project'),
    path('new/', ProjectCreate.as_view(), name='project_new'),
    path('delete/<name>/', ProjectDelete.as_view(), name='project_delete'),
    path('update/<username>/', UserUpdate.as_view(), name='user_update'),
    path('list/', ProjectList.as_view(), name='users_projects'),
    path('members/', ProjectMemberList.as_view(), name='project_members')
]

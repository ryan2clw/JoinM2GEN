from django.shortcuts import render, reverse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from django_tables2 import RequestConfig
# PROJECT SPECIFIC MODULES
from .serializers import ProjectSerializer, UserSerializer, ProjectMemberSerializer
from .models import Project
from .forms import UserAddForm, InviteForm, UserDeleteForm
from .tables import ProjectTable, UserTable

class CustomLoginview(LoginView):
    
    # if they are a customer with project, go there, developer with a project, go there, else, make-project page
    def get_redirect_url(self):
        if(self.request.user.is_anonymous):
            return reverse('login')
        myProjects = Project.objects.filter(members=self.request.user)
        if self.request.user.groups.filter(name="customer").exists() and len(myProjects) > 0:
            return reverse('bill') + "?project=" + myProjects.last().name 
        if self.request.user.groups.filter(name="developer").exists() and len(myProjects) > 0:
            return reverse('clockin')
        return reverse('project')

class ProjectView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'AWSEnroll/index.html'

    def get_context_data(self, **kwargs): 
        context = super(ProjectView, self).get_context_data(**kwargs)
        context['first_name'] = self.request.user.first_name
        context['myForm'] = UserAddForm()
        context['user_email'] = self.request.user.username        
        context['hasProjects'] = "false"
        deleteForm = UserDeleteForm()
        context['deleteForm'] = deleteForm
        if len(self.object_list) > 0:
            context['hasProjects'] = "true"
        try:
        	# PARAMETER 'PROJECT' HELPS FORM USER LIST (USER MODE)
            myProject = Project.objects.filter(name=self.request.GET['project'])[0]
            context['hasProjects'] = "true"
            myUsers = myProject.members.all()
            context['currentID'] = myProject.id
            context['currentProject'] = myProject.name
            context['inviteForm'] = InviteForm()
            table = UserTable(myUsers)
            context['table'] = table
        except:
        	# NO PARAMETER SPECIFIED IS LIKE PROJECT MODE
            table = ProjectTable(self.object_list)
            table.requestor = self.request.user.username
            RequestConfig(self.request, paginate=False).configure(table)
            context['table'] = table
        return context

    def get_queryset(self):
        return Project.objects.filter(members__id=self.request.user.id)

    def form_valid(self, form):
        ''' Begin reCAPTCHA validation '''
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        response = requests.post(url, values)
        ''' End reCAPTCHA validation '''
        if response.ok:
            super(ProjectView, self).form_valid(form)
        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.') 

class ProjectMemberList(ListAPIView):

    serializer_class = ProjectMemberSerializer
    model = Project
    permission_classes = [ permissions.IsAuthenticated, ]

    def get_queryset(self):
        user = User.objects.get(username=self.request.GET["username"])
        return Project.objects.filter(members__id=user.id)

class ProjectList(ListAPIView):

    serializer_class = ProjectSerializer
    model = Project
    permission_classes = [ permissions.IsAuthenticated, ]

    def get_queryset(self):
        user = User.objects.get(username=self.request.GET["username"])
        return Project.objects.filter(members__id=user.id)


class ProjectCreate(CreateAPIView):
    
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()

class ProjectDelete(DestroyAPIView):

    serializer_class = ProjectSerializer
    lookup_field = 'name'

    def get_queryset(self):
        return Project.objects.all()

class UserUpdate(UpdateAPIView):

    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_queryset(self):
        return User.objects.all()






import django_tables2 as tables
from .models import Project
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

class ProjectTable(tables.Table):

    buttons = tables.LinkColumn(empty_values=(), verbose_name='Action')
    requestor = 'IDFK' # Default value is for Anonymous requests
    
    class Meta:
        model = Project
        fields = ('name', 'members', 'buttons')

    def render_buttons(self, record):
        if record.owner.username == self.requestor:
            return mark_safe('<button onclick="deleteProject(event)" class="btn-sm btn-danger whiteBold">Delete</button>')
        return mark_safe('<button onclick="userQuits(event)" class="btn-sm btn-warning grayText">Quit</button>')

class UserTable(tables.Table):

    buttons = tables.LinkColumn(empty_values=(), verbose_name='Action')

    class Meta:
        model = User
        fields = ('username','buttons')

    def render_buttons(self, record):
        return mark_safe('<button onclick="deleteUser(event)" class="btn-sm btn-danger">Delete</button>')
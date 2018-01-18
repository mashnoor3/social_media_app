from django.shortcuts import render

from django.auth.mixins.auth.mixins import (LoginRequiredMixin,
                                            PermissionRequiredMixin)
from django.core.urlresolvers import reverse
from django.views import generic

from groups.models import Group,GroupMember

class CreateGroup(LoginRequiredMixin,generic.CreateView):
    # Users should only be able to modify these two attributes of a group
    fields = ('name','description')
    # Connect to the group model
    model = Group

# Details of the single view
class SingleGroup (generic.DetailView):
    model = Group

class ListGroups(generic.ListView):
    model = Group

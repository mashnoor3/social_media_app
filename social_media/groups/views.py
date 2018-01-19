from django.shortcuts import render
from django.contrib import messages

from django.contrib.auth.mixins import (LoginRequiredMixin,
                                            PermissionRequiredMixin)
from django.core.urlresolvers import reverse
from django.views import generic
from django.shortcuts import get_object_or_404

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

class JoinGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('grpups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,self.kwargs.get('slug'))

        try:
            # try to get the group member object, and create based on user and the group
            GroupMember.objects.create(user=self.request.user, group=group)
        except IntegrityError:
            messages.warning(self.request,'Warning. Already a member')
        else:
            messages.succcess(self.request,'You are now a member')
        return super().get(request,*args,**kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('grpups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        try:
            membership = models.GroupMember.objects.fitler(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,'Sorry you are not in this group.')
        else:
            membership.delete()
            messages.succcess(self.request,'You have left the group.')
        return super().get(request,*args,**kwargs)

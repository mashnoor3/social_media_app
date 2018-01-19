from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy

from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

from . import models
from . import forms

from django.contrib.auth import get_user_model
User = get_user_model()

class PostList(SelectRelatedMixin, generic.ListView):

    model = models.Post
    # Mixin that allows to provide a tuple of related models. Basically the foreign keys for the post.
    select_related =('user', 'group')

# Class for connecting posts and users
class UserPosts(generic.ListView):

    model = models.Post
    template_name = 'post/user_post_list.html'

    def get_queryset(self):
        try:
            # set user of this post to the user's objects and prefetch the user's posts
            # bascially feth posts that are related to the user
            self.post.user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        # return the user who posted
        return context

# Detail view for a singular post
class PostDetail(SelectRelatedMixin, generic.DetailView):

    model = models.Post
    # connect select_related to some foreign keys
    select_related = ('user', 'group')

    def get_queryset(self):
        # get queryset for the post
        queryset = super().get_queryset()
        # filter the quesryset with the user's username
        return quesryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):

    fields = ('message','group')
    model = models.Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.object.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):

    model = models.Post
    select_related = ('user','group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

        def delete(self,*args,**kwargs):
            messages.success(self.request,'Post Deleted')
            return super().delete(*args,**kwargs)

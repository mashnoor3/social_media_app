from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

import misaka

from groups.models import  Group

from django.contrib.auth import get_user_model
# get the current user logged into the session
User = get_user_model()

class Post(models.Model):
    # to do: set up attribute, save method, string method, get absolute url method (once someone has posted something, where to send them), and Meta
    user = models.ForeignKey(User,related_name='posts')
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group,related_name='posts',null=True,blank=True)

    def __str__(self):
        return self.message

    def save(self,*args,**kwargs):
        # So if ppl has markdowns (ie links) in their post doesn't include all the HTML tags
        self.message_html=misaka.html(self.message)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        # two params: URL and the keyword dict
        return reverse('posts:single',kwargs={'username':self.user.username,
                                                'pk':self.pk})

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user','message']

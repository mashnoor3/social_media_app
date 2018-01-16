from django.db import models
from django.contrib import auth


class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        # auth.models.User has a username attribute
        return "@{}".format(self.username)

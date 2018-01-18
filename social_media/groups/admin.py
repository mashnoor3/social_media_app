from django.contrib import admin
from . import models

# Using inline, allows to edit model on the same page as the parent model
# GroupMember's parent model is Group
class GroupMemberInline(admin.TabularInline):
    model = models.GroupMember

admin.site.register(models.Group)

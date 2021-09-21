from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.reverse_related import ManyToOneRel
# Create your models here.

class Task(models.Model):
    # One to many relationship one User can have many items
    # on_delete means what do we do if user gets deleted (what happens to the task)
    # models.CASCADE (Deletes items if user is deleted)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']
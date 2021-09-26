from import_export import resources
from .models import Task

class TaskResource(resources.ModelResource):
    class Meta:
        model = Task
        fields = ['title','description', 'complete', 'created']

        
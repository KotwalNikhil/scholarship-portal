from import_export import resources
from django.contrib.auth.models import User
from .models import profile

class profileResource(resources.ModelResource):
    class Meta:
        model = profile

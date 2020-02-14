from django.contrib import admin
from .models import student,staff,UserProfile
# Register your models here.
admin.site.register(student)
admin.site.register(staff)
admin.site.register(UserProfile)


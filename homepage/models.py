from django.db import models
from datetime import datetime,date


class scholarship(models.Model):
    title=models.CharField(max_length=30)
    applicants=models.IntegerField()
    short_description= models.CharField(max_length=50)
    long_description=models.TextField()
    img=models.ImageField(upload_to='pics/scholarship_pics',default='pics/scholarship_pics/default.png')
    boy=models.BooleanField(default=False)
    girl = models.BooleanField(default=False)
    both = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    document = models.FileField(upload_to='documents/scholarship_broucher/')
    fromdate=models.DateField(null=True)
    toomdate = models.DateField(null=True)


class application_table(models.Model):
    scholarship_id=models.IntegerField(default=0)
    user_id=models.IntegerField(default=0)
    status = models.IntegerField(default=2,blank=True,null=True)
    applied_student_id = models.FileField(upload_to='applications/student_id',blank=True,null=True)
    applied_father_id = models.FileField(upload_to='applications/father_id',blank=True,null=True)
    applied_document_last_sem = models.FileField(upload_to='applications/document_last_sem',blank=True,null=True)
    applied_document12 = models.FileField(upload_to='applications/document12',blank=True,null=True)
    applied_document10 = models.FileField(upload_to='applications/document10',blank=True,null=True)
    applied_extra1 = models.FileField(upload_to='applications/extra1',blank=True,null=True)
    applied_extra2 = models.FileField(upload_to='applications/extra2',blank=True,null=True)





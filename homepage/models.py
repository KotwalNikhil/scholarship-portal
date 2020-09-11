from django.db import models
from datetime import datetime,date

from django.core.exceptions import ValidationError


def file_size(value): # add this to some file where you can import it from
    limit =  1024*1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 1 MB.')

    if not value.path.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise ValidationError('File format is not correct , only png, jpg, or jpeg allowed')

def file_size2(value): # add this to some file where you can import it from
    limit =  1024*1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 1 MB.')

    if not value.path.lower().endswith('.pdf'):
        raise ValidationError('File format is not correct, Only pdf allowed ')



class scholarship(models.Model):
    title=models.CharField(max_length=30)
    short_description= models.CharField(max_length=100)
    long_description=models.TextField()
    img=models.ImageField(upload_to='pics/scholarship_pics',default='pics/scholarship_pics/default.png',validators=[file_size])
    both = models.IntegerField(blank=True,null=True,default=0)
    boy=models.IntegerField(blank=True,null=True,default=-1)
    girl = models.IntegerField(blank=True,null=True,default=-1)
    active = models.BooleanField(default=True)
    document = models.FileField(upload_to='documents/scholarship_broucher/',validators=[file_size2])
    scholarship_form = models.FileField(upload_to='documents/scholarship_form/',default='documents/scholarship_form/default_scholarship_form.pdf',validators=[file_size2])
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
    applied_extra1 = models.FileField(upload_to='applications/extra1',blank=True,null=True,validators=[file_size])
    applied_extra2 = models.FileField(upload_to='applications/extra2',blank=True,null=True,validators=[file_size])
    applied_scholarship_form = models.FileField(upload_to='applications/applied_scholarship_form',blank=True,null=True,validators=[file_size2])



class session_table(models.Model):
    user_id = models.IntegerField(default=0)
    scholarship_id = models.IntegerField(default=0)
    session = models.IntegerField(default=0)

class current_session(models.Model):
    session=models.IntegerField(default=0)



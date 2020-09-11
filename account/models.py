from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.exceptions import ValidationError

def file_size(value): # add this to some file where you can import it from
    limit =  1024*1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 1 MB.')

    if not value.path.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise ValidationError('File format is not correct , only png, jpg, or jpeg allowed')




RANK_COHICES = (
    ('Lance Naik','Lance Naik'),
    ('Naik','Naik'),
    ('Hawaldar','Hawaldar'),
    ('Nb Subedar','Nb Subedar'),
    ('Subedar','Subedar'),
    ('Subeder Maj','Subeder Maj'),
    ('Officer','Officer'),
)
present_year = (
    ('FE','FE'),
    ('SE','SE'),
    ('TE','TE'),
    ('BE','BE'),

)


# Create your models here.
class student(models.Model):
    reg_no=models.IntegerField(validators=[
            MinValueValidator(10000),
            MaxValueValidator(20000)])
    name=models.CharField(max_length=20)
    email=models.EmailField(max_length=250)
    is_verified=models.BooleanField(default=False)



class staff(models.Model):
    emp_no=models.IntegerField(validators=[
            MinValueValidator(10000),
            MaxValueValidator(20000)])
    name=models.CharField(max_length=20)
    branch = models.IntegerField(default=0,validators=[
           MinValueValidator(1),
           MaxValueValidator(5)])

    email=models.EmailField(max_length=250)
    is_verified=models.BooleanField(default=False)

class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    branch=models.IntegerField(default=0)
    division=models.IntegerField(default=0)
    mobile = models.CharField(max_length=50,blank=True,null=True)
    name = models.CharField(max_length=20,default='')
    marks=models.IntegerField(default=0,blank=True,null=True)
    father_rank=models.CharField(max_length=50,choices=RANK_COHICES,default='Officer')
    father_name=models.CharField(max_length=30,default='',blank=True,null=True)
    present_year=models.CharField(max_length=30,choices=present_year,default='FE')

    attendence=models.IntegerField(default=0,blank=True,null=True)


    image= models.ImageField(upload_to='pics/profile_pics',default='pics/profile_pics/default.png',validators=[file_size])
    roll_no=models.IntegerField(default=0)
    address=models.CharField(max_length=50,default='')
    document10 = models.FileField(upload_to='documents/user_documents/10marksheets',blank=True,null=True,validators=[file_size])
    document12 = models.FileField(upload_to='documents/user_documents/12marksheets',blank=True,null=True,validators=[file_size])
    document_last_sem = models.FileField(upload_to='documents/user_documents/last_marksheets',blank=True,null=True,validators=[file_size])
    father_id = models.FileField(upload_to='documents/user_documents/father_id',blank=True,null=True,validators=[file_size])
    student_id = models.FileField(upload_to='documents/user_documents/student_id',blank=True,null=True,validators=[file_size])





    def __str__(self):
        return f'{self.user.username} profile'

@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_profile(sender,instance,**kwargs):
    instance.profile.save()








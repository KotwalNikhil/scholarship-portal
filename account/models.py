from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
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

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    reg_no = models.IntegerField(validators=[
        MinValueValidator(10000),
        MaxValueValidator(20000)])
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=250)
    image= models.ImageField(upload_to='profile_pics',default='pics/default.png')


    def __str__(self):
        return self.user.username




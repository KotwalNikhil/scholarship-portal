from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
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




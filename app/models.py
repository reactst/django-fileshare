from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.



class User(AbstractUser):
    roles = (('s', 'student'), ('p', 'professor'), ('a', 'admin'))
    role = models.CharField(max_length=1, choices=roles, name='role', null=False, default='a')
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'role']



class Documents(models.Model):
    title = models.CharField(max_length=64)
    doc_path = models.CharField(max_length=300)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    doc = models.FileField(max_length=254, null=True, blank=True)


class StudentDocument(models.Model):
    document = models.ForeignKey(Documents, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)

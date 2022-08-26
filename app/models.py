from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

class UploadPermission(models.Model):
    Token = models.CharField(max_length=50)
    DateTime = models.DateTimeField(auto_now=True)
    Used = models.BooleanField(default=False)
    Downloaded = models.BooleanField(default=False)

class AuthUser(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Password = models.CharField(max_length=100)

class AuthorizeUser(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Password = models.CharField(max_length=100)
    UserToken = models.CharField(max_length=50)

class DownloadPermit(models.Model):
    auto_increment_id = models.AutoField(primary_key=True)
    Filename = models.CharField(max_length=100)
    Created = models.DateTimeField(auto_now=True)
    Downloaded = models.BooleanField(default=False)
    FileToken = models.CharField(max_length=50)

 
class MyUserManager(BaseUserManager):
   def create_user(self, email,password, name, token):
       """
       Creates and saves a User with the given email,and password.
       """
       if not email:
           raise ValueError('Users must have an email address')
 
       print("Here")
       user = self.model(email=self.normalize_email(email))
       user.set_password(password)
       user.Name = name
       user.UserToken = token
       user.save(using=self._db)
       return user
 
   def create_superuser(self,name,token, email,password=None):
       """
       Creates and saves a superuser with the given email, date of
       birth and password.
       """
       print("here")
       user = self.create_user(email,name,token,password=password)
       user.is_admin = True
       user.save()
       return user
 


# UserManager class code here
class User(AbstractBaseUser):
    Email = models.EmailField(verbose_name='email address', unique=True,)
    Name = models.CharField(max_length=100)
    UserToken = models.CharField(max_length=50)
    objects = MyUserManager()

    USERNAME_FIELD = 'Email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.Email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
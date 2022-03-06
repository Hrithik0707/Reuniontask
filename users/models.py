from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email,  first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email,first_name, password, **other_fields)

    def create_user(self, email, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email,first_name=first_name,is_active=True, **other_fields)
        user.set_password(password)
        user.save()
        Profile.objects.create(user=user)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def _str_(self):
        return self.email

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='followers',blank=True)
    followings = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='followings',blank=True)


class Post(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100,blank=True)
    description = models.TextField(blank=True,default='')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='posts',on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='likes',blank=True)

    class Meta:
        ordering = ('-created_time',)


class Comment(models.Model):
    comment = models.TextField(blank=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="comments",on_delete=models.CASCADE)
    post = models.ForeignKey(Post,related_name="comments",on_delete=models.CASCADE)

    
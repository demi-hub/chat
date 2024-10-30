from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from .managers import CustomUserManager


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, blank=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    dob = models.DateField(max_length=8, null=False, blank=False)
    city = models.CharField(blank=False, null=False, max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['dob','first_name', 'city']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_dob(self):
        return self.dob.strftime("%Y-%m-%d")

    def has_perm(self):
        return self.is_superuser

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        return super().has_module_perms(app_label)


class ChatRoom(models.Model):
    room_name= models.CharField(max_length=100,unique=True)
    created_by= models.ForeignKey(User, related_name="created_user",on_delete=models.CASCADE,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, null=True)


class ChatHistory(models.Model):
    sender= models.ForeignKey(User,related_name="history_of_sender",on_delete=models.CASCADE)
    receiver= models.ForeignKey(User,related_name="history_of_receiver",on_delete=models.CASCADE)
    message= models.TextField(null=True)
    image= models.TextField(null=True)
    document= models.TextField(null=True)
    room= models.ForeignKey(ChatRoom,related_name="room_id",on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


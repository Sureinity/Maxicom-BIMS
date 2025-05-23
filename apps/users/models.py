from django.db import models
from django.contrib.auth.models import AbstractUser


def user_profile_picture_path(self, filename):
    return f'profile_pictures/{self.username}/{filename}'

class User(AbstractUser):
    # User role
    ADMIN = 0
    USER = 1
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (USER, 'User'),
    ]

    # User account status
    ACTIVE = 0
    DELETED = 1     # For former users (soft delete)
    
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted'),
    ]

    first_name = None
    last_name = None
    email = None
    date_joined = None

    id = models.AutoField(primary_key=True, db_column='sys_acc_id')
    username = models.CharField(
        max_length=150,
        unique=True,
        db_column='sys_username',
        error_messages={
            'unique': 'A user with that username already exists.',
        },
    )
    password = models.CharField(max_length=128, db_column='sys_password')
    sys_firstname = models.CharField(max_length=150, blank=True)
    sys_lastname = models.CharField(max_length=150, blank=True)
    sys_acc_created = models.DateTimeField(auto_now_add=True)
    sys_acc_updated = models.DateTimeField(auto_now=True)
    sys_acc_role = models.IntegerField(choices=ROLE_CHOICES, default=USER)
    sys_status = models.IntegerField(choices=STATUS_CHOICES, default=ACTIVE)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, null=True, blank=True, default='profile_pictures/profile.png')

    REQUIRED_FIELDS = ['sys_acc_role']
    USERNAME_FIELD = 'username'

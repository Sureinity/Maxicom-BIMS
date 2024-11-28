from django.db import models
from django.contrib.auth.models import AbstractUser

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
    SUSPENDED = 1
    DELETED = 2 # Soft delete
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (SUSPENDED, 'Suspended'),
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
    sys_acc_created = models.DateTimeField(auto_now_add=True) # Automatically set when user is created
    sys_acc_role = models.IntegerField(choices=ROLE_CHOICES, default=USER)
    sys_status = models.IntegerField(choices=STATUS_CHOICE, default=ACTIVE)

    REQUIRED_FIELDS = ['sys_acc_role']
    USERNAME_FIELD = 'username'

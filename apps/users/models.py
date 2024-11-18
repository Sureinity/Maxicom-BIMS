from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
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
    sys_acc_role = models.CharField(max_length=50)

    REQUIRED_FIELDS = ['sys_acc_role']
    USERNAME_FIELD = 'username'
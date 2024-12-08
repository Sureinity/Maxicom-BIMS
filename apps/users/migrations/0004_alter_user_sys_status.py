# Generated by Django 5.1.2 on 2024-12-08 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_sys_acc_created_user_sys_acc_updated_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sys_status',
            field=models.IntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0),
        ),
    ]
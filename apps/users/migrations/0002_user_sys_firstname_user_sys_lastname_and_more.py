# Generated by Django 5.1.2 on 2024-11-20 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sys_firstname',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='user',
            name='sys_lastname',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='user',
            name='sys_acc_role',
            field=models.IntegerField(choices=[(0, 'Admin'), (1, 'User')], default=1),
        ),
    ]

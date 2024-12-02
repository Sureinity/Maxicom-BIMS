# Generated by Django 5.1.2 on 2024-12-02 03:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_inventory', '0002_alter_inventory_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booklist',
            name='publishercode',
        ),
        migrations.AddField(
            model_name='booklist',
            name='copyrightdate',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1800), django.core.validators.MaxValueValidator(2024)]),
        ),
        migrations.AddField(
            model_name='booklist',
            name='publisher_code',
            field=models.CharField(blank=True, db_column='b_publisher_code', max_length=255),
        ),
    ]
# Generated by Django 5.1.2 on 2024-12-04 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_inventory', '0004_alter_booklist_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booklist',
            name='date_accessioned',
            field=models.CharField(blank=True, db_column='b_date_accessioned', max_length=55),
        ),
    ]

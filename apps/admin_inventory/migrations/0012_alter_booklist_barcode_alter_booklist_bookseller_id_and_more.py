# Generated by Django 5.1.2 on 2024-12-08 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_inventory', '0011_alter_inventoryhistory_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booklist',
            name='barcode',
            field=models.CharField(db_column='b_barcode', max_length=255),
        ),
        migrations.AlterField(
            model_name='booklist',
            name='bookseller_id',
            field=models.CharField(db_column='b_bookseller_id', max_length=255),
        ),
        migrations.AlterField(
            model_name='booklist',
            name='col_code',
            field=models.CharField(db_column='b_col_code', max_length=255),
        ),
        migrations.AlterField(
            model_name='booklist',
            name='copy_num',
            field=models.CharField(blank=True, db_column='b_copy_num', help_text='Copy number starting from 1', max_length=255),
        ),
        migrations.AlterField(
            model_name='booklist',
            name='copyrightdate',
            field=models.CharField(blank=True, db_column='b_copyrightdate', max_length=255),
        ),
        migrations.AlterField(
            model_name='booklist',
            name='date_accessioned',
            field=models.CharField(blank=True, db_column='b_date_accessioned', max_length=255),
        ),
        migrations.AlterField(
            model_name='booklist',
            name='isbn',
            field=models.CharField(db_column='b_isbn', max_length=255),
        ),
        migrations.AlterField(
            model_name='booklist',
            name='item_call_num',
            field=models.CharField(db_column='b_item_call_num', max_length=255),
        ),
        migrations.AlterField(
            model_name='booklist',
            name='itype',
            field=models.CharField(db_column='b_itype', max_length=255),
        ),
        migrations.AlterField(
            model_name='booklist',
            name='paidfor',
            field=models.CharField(blank=True, db_column='b_paidfor', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='booklist',
            name='price',
            field=models.CharField(blank=True, db_column='b_price', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='booklist',
            name='volume',
            field=models.CharField(blank=True, db_column='b_volume', max_length=255, null=True),
        ),
    ]

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import datetime

from apps.users.models import User

# Create your models here.

class Booklist(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="b_id")
    item_call_num = models.CharField(max_length=200, blank=False, db_column="b_item_call_num")
    col_code = models.CharField(max_length=100, blank=False, db_column="b_col_code")
    barcode = models.CharField(max_length=55, blank=False, db_column="b_barcode")
    itype = models.CharField(max_length=100, blank=False, db_column="b_itype")
    title = models.CharField(max_length=255, blank=False, db_column="b_title")
    author = models.CharField(max_length=255, blank=False, db_column="b_author")
    publisher_code = models.CharField(max_length=255, blank=True, db_column="b_publisher_code")
    date_accessioned = models.CharField(max_length=55, blank=True, db_column="b_date_accessioned")
    copyrightdate = models.CharField(max_length=55, blank=True, db_column="b_copyrightdate")
    isbn = models.CharField(max_length=20, blank=False, db_column="b_isbn")
    copy_num = models.CharField(max_length=55, db_column="b_copy_num", blank=True,  help_text="Copy number starting from 1")
    volume = models.CharField(max_length=100, blank=True, null=True, db_column="b_volume")
    edition_stmt = models.CharField(max_length=255, blank=True, null=True, db_column="b_edition_stmt")
    subtitle = models.TextField(db_column="b_subtitle", blank=True, null=True)
    paidfor = models.CharField(max_length=55, blank=True, null=True, db_column="b_paidfor")
    price = models.CharField(max_length=55, null=True, blank=True, db_column="b_price") # PHP Peso
    bookseller_id = models.CharField(max_length=55, blank=False, db_column="b_bookseller_id")

    class Meta:
        ordering = ['title']
        
class Inventory(models.Model):
    # Book status
    GOOD_CONDITION = 1
    NO_BARCODE_TAG = 2
    FOR_REPAIR = 3
    FOR_DISPOSAL = 4

    BOOK_STATUS_CHOICES = [
        (GOOD_CONDITION, 'Good Condition'),
        (NO_BARCODE_TAG, 'No Barcode Tag'),
        (FOR_REPAIR, 'For Repair'),
        (FOR_DISPOSAL, 'For Disposal'),
    ]

    id = models.BigAutoField(primary_key=True, db_column="inv_id")
    book = models.ForeignKey(Booklist, on_delete=models.CASCADE)
    datetime_checked = models.DateTimeField(auto_now=True, db_column="inv_datetime_checked")
    status =  models.IntegerField(choices=BOOK_STATUS_CHOICES, null=True, blank=True, db_column="inv_status")

    class Meta:
        ordering = ['-datetime_checked']

# Partial model layout for InventoryHistory
class InventoryHistory(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="h_id")
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="history")
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column="h_reviewed_by")
    datetime_checked = models.DateTimeField(auto_now=True, db_column="h_datetime_checked")
    status = models.IntegerField(
        choices=Inventory.BOOK_STATUS_CHOICES,
        db_column="h_status"
    )

    class Meta:
        ordering = ['-datetime_checked']
        indexes = [
            models.Index(fields=['inventory']),
            models.Index(fields=['reviewed_by']),
        ]
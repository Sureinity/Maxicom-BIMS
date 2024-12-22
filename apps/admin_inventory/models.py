from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import datetime

from apps.users.models import User

class Booklist(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="b_id")
    item_call_num = models.CharField(max_length=255, blank=False, unique=True, db_column="b_item_call_num") # Unique
    decimal_part = models.FloatField(null=True, blank=True, db_column="b_decimal_part")  # Store decimal part
    col_code = models.CharField(max_length=255, blank=False, db_column="b_col_code") 
    barcode = models.CharField(max_length=255, blank=False, unique=True, db_column="b_barcode") # Unique
    itype = models.CharField(max_length=255, blank=False, db_column="b_itype")
    title = models.CharField(max_length=255, blank=False, db_column="b_title")
    author = models.CharField(max_length=255, blank=False, db_column="b_author")
    publisher_code = models.CharField(max_length=255, blank=True, db_column="b_publisher_code")
    date_accessioned = models.CharField(max_length=255, blank=True, db_column="b_date_accessioned")
    copyrightdate = models.CharField(max_length=255, blank=True, db_column="b_copyrightdate")
    isbn = models.CharField(max_length=255, blank=False, unique=True, db_column="b_isbn") # Unique
    copy_num = models.CharField(max_length=255, db_column="b_copy_num", blank=True, help_text="Copy number starting from 1")
    volume = models.CharField(max_length=255, blank=True, null=True, db_column="b_volume")
    edition_stmt = models.CharField(max_length=255, blank=True, null=True, db_column="b_edition_stmt")
    subtitle = models.TextField(db_column="b_subtitle", blank=True, null=True)
    paidfor = models.CharField(max_length=255, blank=True, null=True, db_column="b_paidfor")
    price = models.CharField(max_length=255, null=True, blank=True, db_column="b_price")  # PHP Peso
    bookseller_id = models.CharField(max_length=255, blank=False, db_column="b_bookseller_id")

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["isbn"]),
            models.Index(fields=["decimal_part"]),
            models.Index(fields=["col_code"]),
            models.Index(fields=["copyrightdate"]),
        ]
    
    def save(self, *args, **kwargs):
        """Override save method to extract decimal part from item_call_num"""
        if self.item_call_num:
            parts = self.item_call_num.split()
            if len(parts) >= 2:
                try:
                    self.decimal_part = float(parts[1])
                except ValueError:
                    self.decimal_part = None
        if self.isbn:
            self.isbn = ''.join(filter(str.isdigit, self.isbn))
        super().save(*args, **kwargs)
        
class Inventory(models.Model):
    # Status choices
    GOOD_CONDITION = 1
    NO_BARCODE_TAG = 2
    FOR_REPAIR = 3
    FOR_DISPOSAL = 4
    NOT_FOUND = 5

    BOOK_STATUS_CHOICES = [
        (GOOD_CONDITION, 'Good Condition'),
        (NO_BARCODE_TAG, 'No Barcode Tag'),
        (FOR_REPAIR, 'For Repair'),
        (FOR_DISPOSAL, 'For Disposal'),
        (NOT_FOUND, 'Not Found'),
    ]

    id = models.BigAutoField(primary_key=True, db_column="inv_id")
    book = models.ForeignKey(Booklist, on_delete=models.CASCADE, db_index=True, related_name='inventories')  # Add related_name
    datetime_checked = models.DateTimeField(auto_now=True, db_column="inv_datetime_checked", db_index=True)
    status =  models.IntegerField(choices=BOOK_STATUS_CHOICES, default=NOT_FOUND, db_column="inv_status", db_index=True)

    class Meta:
        ordering = ['-datetime_checked']

class InventoryHistory(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="h_id")
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="history")
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE, db_column="h_reviewed_by")
    datetime_checked = models.DateTimeField(auto_now=True, db_column="h_datetime_checked")
    remarks = models.CharField(max_length=110, blank=True, null=True, db_column="h_remarks")
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

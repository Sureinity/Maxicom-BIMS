from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

# Create your models here.

#Partial model layout for Booklist
class Booklist(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="b_id")
    item_call_num = models.CharField(max_length=200, blank=False, unique=True, db_column="b_item_call_num")
    col_code = models.CharField(max_length=100, blank=False, db_column="b_col_code")
    barcode = models.CharField(max_length=55, blank=False, unique=True, db_column="b_barcode")
    itype = models.CharField(max_length=100, blank=False, db_column="b_itype")
    title = models.CharField(max_length=255, blank=False, db_column="b_title")
    author = models.CharField(max_length=255, blank=False, db_column="b_author")
    publishercode = models.CharField(max_length=255, blank=False, db_column="b_publishercode")
    date_accessioned = models.DateField(auto_now=True, db_column="b_date_accessioned")
    isbn = models.CharField(max_length=20, blank=False, db_column="b_isbn")
    copy_num = models.IntegerField(db_column="b_copy_num", validators=[MinValueValidator(1)], help_text="Copy number starting from 1")
    volume = models.CharField(max_length=100, blank=True, null=True, db_column="b_volume")
    edition_stmt = models.CharField(max_length=255, blank=True, null=True, db_column="b_edition_stmt")
    subtitle = models.TextField(db_column="b_subtitle", blank=True, null=True)
    paidfor = models.CharField(max_length=55, blank=True, null=True, db_column="b_paidfor")
    price = models.DecimalField(max_digits=10, decimal_places=2, db_column="b_price") # PHP Peso
    bookseller_id = models.CharField(max_length=55, blank=False, db_column="b_bookseller_id")

    class Meta:
        ordering = ['title']

    def clean(self):
        if self.price and self.price < 0:
            raise ValidationError({'price': 'Price cannot be negative'})
        
        if self.isbn and len(self.isbn.replace('-', '')) not in [10, 13]:
            raise ValidationError({'isbn': 'ISBN must be 10 or 13 digits'})


#Partial model layout for Inventory
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
    b_id = models.ForeignKey(Booklist, on_delete=models.CASCADE)
    datetime_checked = models.DateTimeField(auto_now=True, db_column="inv_datetime_checked")
    status =  models.IntegerField(choices=BOOK_STATUS_CHOICES, null=True, blank=True, db_column="inv_status")

    class Meta:
        ordering = ['-datetime_checked']

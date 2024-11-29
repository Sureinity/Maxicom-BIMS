from django.db import models

# Create your models here.

#Partial model layout for Booklist
class Booklist(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="b_id")
    item_call_num = models.CharField(max_length=200, blank=True, db_column="b_item_call_num")
    col_code = models.CharField(max_length=100, blank=False, db_column="b_col_code")
    barcode = models.CharField(max_length=55, blank=False, db_column="b_barcode")
    itype = models.CharField(max_length=100, blank=False, db_column="b_itype")
    title = models.CharField(max_length=255, blank=False, db_column="b_title")
    author = models.CharField(max_length=255, blank=False, db_column="b_author")
    publishercode = models.CharField(max_length=255, blank=False, db_column="b_publishercode")
    date_accessioned = models.DateField(auto_now=True, db_column="b_date_accessioned")
    isbn = models.IntegerField(db_column="b_isbn")
    copy_num = models.IntegerField(db_column="b_copy_num")
    volume = models.CharField(max_length=100, blank=True, db_column="b_volume")
    edition_stmt = models.CharField(max_length=255, blank=True, db_column="b_edition_stmt")
    subtitle = models.TextField()
    paidfor = models.CharField(max_length=55, blank=True, db_column="b_paidfor")
    price = models.DecimalField(max_digits=10, decimal_places=2, db_column="b_price") # PHP Peso
    bookseller_id = models.CharField(max_length=55, blank=False, db_column="b_bookseller_id")

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
    status =  models.IntegerField(choices=BOOK_STATUS_CHOICES, null=True)

from django.db import models

# Create your models here.

#Partial model layout for Booklist
class Booklist(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="b_id")
    item_call_number = models.CharField(max_length="11", blank=True, db_column="b_col_code")
    barcode = models.IntegerField(db_column="b_barcode")
    col_code = models.CharField(max_length="11", blank=True, db_column="b_col_code")
    title = models.CharField(max_length=255, blank=True, db_column="b_title")
    author = models.CharField(max_length=255, blank=True, db_column="b_author")
    publisher = models.CharField(max_length=255, blank=True, db_column="b_publisher")
    date_pub = models.DateField(auto_now=True, db_column="b_date_pub")
    place_pub = models.CharField(max_length=255, db_column="b_place_pub")
    isbn = models.IntegerField(db_column="b_isbn")
    date_acquired = models.DateField(auto_now=True, db_column="b_date_acquired")
    copy_no = models.IntegerField(db_column="b_copy_no")
    volume_no = models.IntegerField(db_column="b_volume_no")
    edition_stmt = models.CharField(max_length=255, db_column="b_edition_stmt")
    price = models.DecimalField(max_digits=10, decimal_places=2, db_column="b_price")

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
    datetime_checked = models.DatetimeField(auto_now=True, db_column="inv_datetime_checked")
    status =  models.IntegerField(choices=BOOK_STATUS_CHOICES, null=True)





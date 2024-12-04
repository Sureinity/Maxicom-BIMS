from django import forms
from .models import Booklist

class CreateBook(forms.ModelForm):
    class Meta:
        model = Booklist
        fields = ["title", "subtitle", "author", "publisher_code", "copyrightdate", "isbn",
                  "col_code", "itype", "item_call_num", "copy_num", "volume", 
                  "edition_stmt", "paidfor", "price", "bookseller_id"]

 


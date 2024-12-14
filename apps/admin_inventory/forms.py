from django import forms
from .models import Booklist
from django.contrib.auth import get_user_model

class CreateBook(forms.ModelForm):
    class Meta:
        model = Booklist
        fields = ["title", "subtitle", "author", "publisher_code", "copyrightdate", "isbn",
                  "col_code", "itype", "item_call_num", "copy_num", "volume", 
                  "edition_stmt", "paidfor", "price", "bookseller_id"]

class UserProfilePictureForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('profile_picture',)


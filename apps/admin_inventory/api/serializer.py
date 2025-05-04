from rest_framework import serializers
from ..models import Inventory

class BookQuerySerializer(serializers.Serializer):
    title = serializers.CharField(allow_blank=True)
    author = serializers.CharField(allow_blank=True)
    subtitle = serializers.CharField(allow_blank=True)
    publisher_code = serializers.CharField(allow_blank=True)
    itype = serializers.CharField(allow_blank=True)
    isbn = serializers.CharField(allow_blank=True)

class BookFoundAndNotFoundSerializer(serializers.ModelSerializer):
    barcode = serializers.CharField(allow_blank=True, source="book.barcode")
    col_code = serializers.CharField(allow_blank=True, source="book.col_code")
    title = serializers.CharField(allow_blank=True, source="book.title")
    author = serializers.CharField(allow_blank=True, source="book.author")
    status = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = [
            'barcode',
            'col_code',
            'title',
            'author',
            'datetime_checked',
            'status'
        ]
    
    def get_status(self, obj):
        return obj.get_status_display()

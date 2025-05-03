from rest_framework import serializers

class BookQuerySerializer(serializers.Serializer):
    title = serializers.CharField(allow_blank=True)
    author = serializers.CharField(allow_blank=True)
    subtitle = serializers.CharField(allow_blank=True)
    publisher_code = serializers.CharField(allow_blank=True)
    itype = serializers.CharField(allow_blank=True)
    isbn = serializers.CharField(allow_blank=True)



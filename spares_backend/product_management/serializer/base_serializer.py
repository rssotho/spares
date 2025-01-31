from rest_framework import serializers


class CreateCategorySerializer(serializers.Serializer):

    description = serializers.CharField()
    category_name = serializers.CharField()
    file_url = serializers.URLField(
        required = False
    )
from rest_framework import serializers

from product_management.models import (
    Category,
    CategoryProfile
)


class ViewCategoryProfileModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryProfile
        fields = (
            'file_url',
        )


class ViewCategoryModelSerializer(serializers.ModelSerializer):

    file_url = ViewCategoryProfileModelSerializer()

    class Meta:
        model = Category
        fields = (
            'file_url',
            'description',
            'category_name',
        )


















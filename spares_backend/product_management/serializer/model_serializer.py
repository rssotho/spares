from rest_framework import serializers

from product_management.models import (
    Product,
    Category,
    ProductProfile,
    CategoryProfile,
)


class ViewCategoryProfileModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryProfile
        fields = (
            'id',
            'file_url',
            'category_id'
        )


class ViewCategoryModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = (
            'id',
            'user_id',
            'description',
            'category_name',
            'date_created',
            'date_modified',
        )


class ViewProductModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'id',
            'price',
            'user_id',
            'total_items',
            'description',
            'product_name',
            'date_created',
            'date_modified',
        )


class ViewProductProfileModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductProfile
        fields = (
            'id',
            'file_url',
            'product_id'
        )












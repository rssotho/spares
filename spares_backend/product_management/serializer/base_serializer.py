from rest_framework import serializers


class CreateCategorySerializer(serializers.Serializer):

    description = serializers.CharField()
    category_name = serializers.CharField()
    file_url = serializers.URLField(
        required = False
    )


class EditCategorySerializer(serializers.Serializer):

    description = serializers.CharField()
    category_name = serializers.CharField()
    file_url = serializers.URLField(
        required = False
    )
    category_id = serializers.IntegerField()
    category_profile_id = serializers.IntegerField()


class GetCategorySerializer(serializers.Serializer):

    category_id = serializers.IntegerField()


class GetCategoryProfileSerializer(serializers.Serializer):

    category_profile_id = serializers.IntegerField()


class CreateProductSerializer(serializers.Serializer):

    price = serializers.FloatField()
    description = serializers.CharField()
    product_name = serializers.CharField()
    total_items = serializers.IntegerField()
    category_id = serializers.IntegerField()
    total_items = serializers.IntegerField()
    file_url = serializers.URLField(
        required = False
    )


class EditProductSerializer(serializers.Serializer):

    price = serializers.FloatField()
    description = serializers.CharField()
    product_name = serializers.CharField()
    product_id = serializers.IntegerField()
    total_items = serializers.IntegerField()
    file_url = serializers.URLField(
        required = False
    )
    product_profile_id = serializers.IntegerField()


class GetProductSerializer(serializers.Serializer):

    product_id = serializers.IntegerField()


class GetProductProfileSerializer(serializers.Serializer):

    product_profile_id = serializers.IntegerField()






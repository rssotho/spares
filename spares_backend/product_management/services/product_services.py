import json

from rest_framework import status
from rest_framework.response import Response

from product_management.packages.product_packages import(
    ProductManagenentPackages
)
from product_management.serializer.base_serializer import (
    CreateCategorySerializer
)


class ProductManagementServices:

    def __init__(
        self,
        request
    ):

        self.request = request

    def create_category(self):

        data = self.request.data
        user = self.request.user
        serializer: CreateCategorySerializer = CreateCategorySerializer(
            data = data
        )

        if not serializer.is_valid():

            response_data = json.dumps({
                'status': 'error',
                'message': 'Invalied request to API',
                'data': serializer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data:dict = serializer.validated_data
        file_url: str = validated_data.get('file_url')
        description: str = validated_data.get('description')
        category_name: str = validated_data.get('category_name')

        try:

            category = ProductManagenentPackages(
                description = description,
                category_name = category_name
            ).create_category()

            if file_url:

                ProductManagenentPackages(
                    user_id = user,
                    file_url = file_url,
                    category_id = category,
                ).create_category_profile()

            response_data = json.dumps({
                'status': 'success',
                'message': 'Category is created successfully',
                'data': serializer.data
            })
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as message:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to created category',
                'data': str(message)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def edit_category(self):

        data = self.request.data
        serializer: CreateCategorySerializer = CreateCategorySerializer(
            data = data
        )

        if not serializer.is_valid():

            response_data = json.dumps({
                'status': 'error',
                'message': 'Invalied request to API',
                'data': serializer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data:dict = serializer.validated_data
        file_url: str = validated_data.get('file_url')
        description: str = validated_data.get('description')
        category_name: str = validated_data.get('category_name')

        try:

            ProductManagenentPackages(
                description = description,
                category_name = category_name
            ).edit_category()

            if file_url:

                ProductManagenentPackages(
                    file_url = file_url,
                ).edit_category_profile()

            response_data = json.dumps({
                'status': 'success',
                'message': 'Category is updated successfully',
                'data': serializer.data
            })
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as message:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to update category',
                'data': str(message)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def view_category(self):

        pass




















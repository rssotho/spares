import json

from rest_framework import status
from rest_framework.response import Response

from product_management.packages.product_packages import(
    ProductManagenentPackages
)
from product_management.serializer.base_serializer import (
    GetProductSerializer,
    GetCategorySerializer,
    EditProductSerializer,
    EditCategorySerializer,
    CreateProductSerializer,
    CreateCategorySerializer,
    GetCategoryProfileSerializer,
)

from product_management.serializer.model_serializer import (
    ViewProductModelSerializer,
    ViewCategoryModelSerializer,
    ViewCategoryProfileModelSerializer,
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
                user_id = user.id,
                description = description,
                category_name = category_name
            ).create_category()

            if file_url:

                ProductManagenentPackages(
                    file_url = file_url,
                    category_id = category.id,
                ).create_category_profile()

            response_data = json.dumps({
                'status': 'success',
                'message': 'Category is created successfully',
                'data': serializer.data
            })
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as message:

            category.delete()
            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to created category',
                'data': str(message)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def edit_category(self):

        data = self.request.data
        serializer: EditCategorySerializer = EditCategorySerializer(
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
        category_id: str = validated_data.get('category_id')
        category_name: str = validated_data.get('category_name')
        category_profile_id: str = validated_data.get('category_profile_id')

        try:

            ProductManagenentPackages(
                category_id = category_id,
                description = description,
                category_name = category_name
            ).edit_category()

            if file_url:

                ProductManagenentPackages(
                    file_url = file_url,
                    category_profile_id = category_profile_id,
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

        data = self.request.data

        serializer: GetCategorySerializer = GetCategorySerializer(
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
        category_id: int = validated_data.get('category_id')

        try:

            category: ProductManagenentPackages = ProductManagenentPackages(
                category_id = category_id
            ).get_category()

            model_serializer: ViewCategoryModelSerializer = ViewCategoryModelSerializer(
                instance = category,
                many = False
            )

            response_data = json.dumps({
                'status': 'success',
                'message': 'Category is fetched successfully',
                'data': model_serializer.data
            })
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as message:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to fetch category',
                'data': str(message)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def view_categoty_profile(self):

        data = self.request.data

        serializer: GetCategoryProfileSerializer = GetCategoryProfileSerializer(
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
        category_profile_id: int = validated_data.get('category_profile_id')

        try:

            category: ProductManagenentPackages = ProductManagenentPackages(
                category_profile_id = category_profile_id
            ).get_category_profile()

            model_serializer: ViewCategoryProfileModelSerializer = ViewCategoryProfileModelSerializer(
                instance = category,
                many = False
            )

            response_data = json.dumps({
                'status': 'success',
                'message': 'Category is fetched successfully',
                'data': model_serializer.data
            })
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as message:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to fetch category',
                'data': str(message)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def create_product(self):

        data = self.request.data
        user = self.request.user

        serializer: CreateProductSerializer = CreateProductSerializer(
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
        price: float = validated_data.get('price')
        file_url: str = validated_data.get('file_url')
        description: str = validated_data.get('description')
        category_id: int = validated_data.get('category_id')
        total_items: int = validated_data.get('total_items')
        product_name: str = validated_data.get('product_name')

        try:

            product = ProductManagenentPackages(
                price = price,
                user_id = user.id,
                description = description,
                category_id = category_id,
                total_items = total_items,
                product_name = product_name
            ).create_product()

            if file_url:

                ProductManagenentPackages(
                    file_url = file_url,
                    product_id = product.id
                ).create_product_profile()

            response_data = json.dumps({
                'status': 'success',
                'message': 'Product is created successfully',
                'data': serializer.data
            })
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as message:

            product.delete()

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to create product',
                'data': str(message)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def edit_product(self):

        data = self.request.data
        user = self.request.user

        serializer: EditProductSerializer = EditProductSerializer(
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
        price: float = validated_data.get('price')
        description: str = validated_data.get('description')
        product_id: int = validated_data.get('product_id')
        total_items: int = validated_data.get('total_items')
        product_name: str = validated_data.get('product_name')

        try:

            ProductManagenentPackages(
                price = price,
                description = description,
                product_id = product_id,
                total_items = total_items,
                product_name = product_name
            ).edit_product()

            response_data = json.dumps({
                'status': 'success',
                'message': 'Product is updated successfully',
                'data': serializer.data
            })
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as message:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to update product',
                'data': str(message)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def view_product(self):

        data = self.request.data

        serializer: GetProductSerializer = GetProductSerializer(
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
        product_id: int = validated_data.get('product_id')

        try:

            product: ProductManagenentPackages = ProductManagenentPackages(
                product_id = product_id
            ).get_products()

            model_serializer: ViewProductModelSerializer = ViewProductModelSerializer(
                instance = product,
                many = False
            )

            response_data = json.dumps({
                'status': 'success',
                'message': 'Product is fetched successfully',
                'data': model_serializer.data
            })
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as message:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to fetch product',
                'data': str(message)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def view_categories(self):

        try:

            categories: ProductManagenentPackages = ProductManagenentPackages().view_categories()

            model_serializer: ViewCategoryModelSerializer = ViewCategoryModelSerializer(
                instance = categories,
                many = True
            )

            response_data = json.dumps({
                'status': 'success',
                'message': 'Categories are fetched successfully',
                'data': model_serializer.data
            })
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as message:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to fetch categories',
                'data': str(message)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def view_products(self):

        try:

            products: ProductManagenentPackages = ProductManagenentPackages().view_products()

            model_serializer: ViewProductModelSerializer = ViewProductModelSerializer(
                instance = products,
                many = True
            )

            response_data = json.dumps({
                'status': 'success',
                'message': 'Products are fetched successfully',
                'data': model_serializer.data
            })
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as message:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to fetch products',
                'data': str(message)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)









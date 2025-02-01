from rest_framework.decorators import (
    api_view,
)

from global_app import constants as constant
from global_app.roles_required import roles_required

from product_management.services.product_services import ProductManagementServices


@api_view(['POST'])
@roles_required(
    constant.SYSTEM_ADMIN,
)
def create_category(request):

    response = ProductManagementServices(
        request = request
    ).create_category()

    return response


@api_view(['POST'])
@roles_required(
    constant.SYSTEM_ADMIN,
)
def edit_category(request):

    response = ProductManagementServices(
        request = request
    ).edit_category()

    return response


@api_view(['GET'])
@roles_required(
    constant.SYSTEM_ADMIN,
)
def view_category(request):

    response = ProductManagementServices(
        request = request
    ).view_category()

    return response



@api_view(['GET'])
@roles_required(
    constant.SYSTEM_ADMIN,
)
def view_categoty_profile(request):

    response = ProductManagementServices(
        request = request
    ).view_categoty_profile()

    return response


@api_view(['POST'])
@roles_required(
    constant.SYSTEM_ADMIN,
)
def create_product(request):

    response = ProductManagementServices(
        request = request
    ).create_product()

    return response


@api_view(['POST'])
@roles_required(
    constant.SYSTEM_ADMIN,
)
def edit_product(request):

    response = ProductManagementServices(
        request = request
    ).edit_product()

    return response


@api_view(['GET'])
@roles_required(
    constant.SYSTEM_ADMIN,
)
def view_product(request):

    response = ProductManagementServices(
        request = request
    ).view_product()

    return response


@api_view(['GET'])
@roles_required(
    constant.CUSTOMER,
    constant.SYSTEM_ADMIN,
)
def view_categories(request):

    response = ProductManagementServices(
        request = request
    ).view_categories()

    return response


@api_view(['GET'])
@roles_required(
    constant.CUSTOMER,
    constant.SYSTEM_ADMIN,
)
def view_products(request):

    response = ProductManagementServices(
        request = request
    ).view_products()

    return response


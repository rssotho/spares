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
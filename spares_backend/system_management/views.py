from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import AllowAny

from global_app import constants as constant
from global_app.roles_required import roles_required

from system_management.services.user_management import UserManagementServices


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def sign_up(request):

    response = UserManagementServices(
        request = request
    ).sign_up()

    return response


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def user_login(request):

    response = UserManagementServices(
        request = request
    ).user_login()

    return response


@api_view(['POST'])
@roles_required(
    constant.CUSTOMER,
    constant.SYSTEM_ADMIN,
)
def create_profile(request):

    response = UserManagementServices(
        request = request
    ).create_profile()

    return response


@api_view(['POST'])
@roles_required(
    constant.CUSTOMER,
    constant.SYSTEM_ADMIN,
)
def edit_profile(request):

    response = UserManagementServices(
        request = request
    ).edit_profile()

    return response


@api_view(['GET'])
@roles_required(
    constant.CUSTOMER,
    constant.SYSTEM_ADMIN,
)
def view_profile(request):

    response = UserManagementServices(
        request = request
    ).view_profile()

    return response


@api_view(['POST'])
@roles_required(
    constant.CUSTOMER,
    constant.SYSTEM_ADMIN,
)
def create_otp(request):

    response = UserManagementServices(
        request = request
    ).create_otp()

    return response


@api_view(['POST'])
@roles_required(
    constant.CUSTOMER,
    constant.SYSTEM_ADMIN,
)
def resend_otp(request):

    response = UserManagementServices(
        request = request
    ).resend_otp()

    return response


@api_view(['POST'])
@roles_required(
    constant.CUSTOMER,
    constant.SYSTEM_ADMIN,
)
def verify_otp(request):

    response = UserManagementServices(
        request = request
    ).verify_otp()

    return response


@api_view(['POST'])
@roles_required(
    constant.SYSTEM_ADMIN,
)
def create_user(request):

    response = UserManagementServices(
        request = request
    ).create_user()

    return response


@api_view(['POST'])
@roles_required(
    constant.SYSTEM_ADMIN,
)
def edit_user(request):

    response = UserManagementServices(
        request = request
    ).edit_user()

    return response


@api_view(['GET'])
@roles_required(
    constant.SYSTEM_ADMIN,
)
def view_customer(request):

    response = UserManagementServices(
        request = request
    ).view_customer()

    return response


@api_view(['GET'])
@roles_required(
    constant.SYSTEM_ADMIN,
)
def view_users(request):

    response = UserManagementServices(
        request = request
    ).view_users()

    return response


@api_view(['GET'])
@roles_required(
    constant.SYSTEM_ADMIN,
)
def view_admin(request):

    response = UserManagementServices(
        request = request
    ).view_admin()

    return response


@api_view(['GET'])
@roles_required(
    constant.SYSTEM_ADMIN,
)
def view_customer(request):

    response = UserManagementServices(
        request = request
    ).view_customer()

    return response


@api_view(['GET'])
@roles_required(
    constant.CUSTOMER,
    constant.SYSTEM_ADMIN,
)
def user_logout(request):

    response = UserManagementServices(
        request = request
    ).user_logout()

    return response


@api_view(['POST'])
@roles_required(
    constant.CUSTOMER,
    constant.SYSTEM_ADMIN,
)
def reset_password(request):

    response = UserManagementServices(
        request = request
    ).reset_password()

    return response


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def forgot_password(request):

    response = UserManagementServices(
        request = request
    ).forgot_password()

    return response


@api_view(['POST'])
@roles_required(
    constant.CUSTOMER,
    constant.SYSTEM_ADMIN,
)
def change_password(request):

    response = UserManagementServices(
        request = request
    ).change_password()

    return response















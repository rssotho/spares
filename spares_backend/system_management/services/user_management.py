import json
import string
import secrets
import threading

from datetime import (
    timedelta
)

from decouple import config

from django.utils import timezone
from django.contrib.auth import (
    login,
    logout,
    authenticate
)

from rest_framework import status
from rest_framework.response import Response

from global_app import constants as constant
from global_app.send_email import send_email_api

from system_management.packages.user_management import UserManagementPackage
from system_management.serializer.base_serializer import (
    LoginSerializer,
    SignUpSerializer,
    EditUserSerializer,
    ResendOTPSerializer,
    VerifyOTPSerializer,
    CreateUserSerializer,
    EditProfileSerializer,
    CreateProfileSerializer,
    ResetPasswordSerializer,
    ForgotPasswordSerializer,
    ChangePasswordSerializer,
)
from system_management.serializer.model_serializer import (
    ViewUserModelSerializer,
    ViewProfileModelSerializer,
)


class UserManagementServices:

    def __init__(
        self,
        request,
        global_frontend_url = config('GLOBAL_FRONTEND_URL')
    ):

        self.request = request
        self.global_frontend_url = global_frontend_url

    @staticmethod
    def generate_password():

        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for _ in range(8))

        return password

    @staticmethod
    def generate_otp():

        otp_code = ''.join(secrets.choice(string.digits) for _ in range(6))

        return otp_code

    @staticmethod
    def generate_time():

        expires_at = timezone.now() + timedelta(minutes = 15)

        return expires_at

    def sign_up(self):

        data = self.request.data

        serializer:SignUpSerializer = SignUpSerializer(
            data = data
        )

        if not serializer.is_valid():

            response_data = json.dumps({
                'status': 'error',
                'message': 'Invalid request to API',
                'data': serializer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data:dict = serializer.validated_data
        email: str = validated_data.get('email')
        password: str = validated_data.get('password')
        last_name: str = validated_data.get('last_name')
        first_name: str = validated_data.get('first_name')
        phone_number: int = validated_data.get('phone_number')

        role = UserManagementPackage().get_role()

        try:

            check_email = UserManagementPackage(
                email = email
            ).check_email()

            if check_email:

                response_data = json.dumps({
                    'status': 'error',
                    'message': 'Email already exists, please provide a different email'
                })
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            check_phone_number = UserManagementPackage(phone_number = phone_number).check_phone_number()

            if check_phone_number:

                response_data = json.dumps({
                    'status': 'error',
                    'message': 'Phone Number already exists, please provide a different phone number'
                })
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            UserManagementPackage(
                email = email,
                password = password,
                last_name = last_name,
                first_name = first_name,
                phone_number = phone_number,
                role_id = role.id
            ).sign_up()

            response_data = json.dumps({
                'status': 'success',
                'message': 'Successfully signed up',
                'data': serializer.data
            })
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as message:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to sign up the user',
                'data': str(message)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def user_login(self):

        data = self.request.data
        serializer: LoginSerializer = LoginSerializer(
            data = data
        )

        if not serializer.is_valid():

            response_data = json.dumps({
                'status': 'error',
                'message': 'Invalid request to API',
                'data': serializer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data: dict = serializer.validated_data
        email: str = validated_data.get('email')
        password: str = validated_data.get('password')
        phone_number: int = validated_data.get('phone_number')

        if not (email or phone_number):

            response_data = json.dumps({
                'status': 'info',
                'message': 'Email or Phone Number is required'
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        user_management: UserManagementPackage = UserManagementPackage(
            email=email,
            phone_number=phone_number,
            password=password
        )

        try:

            user = user_management.user_login()

            if not user:

                response_data = json.dumps({
                    'status': 'error',
                    'message': 'Invalid credentials, please enter the correct details'
                })
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            user = authenticate(
                self.request,
                email = email,
                password = password,
                phone_number = phone_number
            )

            if user is None:

                response_data = json.dumps({
                    'status': 'error',
                    'message': 'Invalid credentials, please enter the correct details'
                })
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            login(
                self.request,
                user
            )

            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])

            token = user_management.create_token(user)

            user_details = {
                'email': user.email,
                'role': user.role.role,
                'last_name': user.last_name,
                'first_name': user.first_name,
                'phone_number': user.phone_number,
            }

            response_data = json.dumps({
                'status': 'success',
                'message': 'User logged in successfully',
                'data': {
                    'token': token.key,
                    'user_details': user_details,
                }
            })
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as message:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to login user',
                'data': str(message)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def create_profile(self):

        data = self.request.data
        user = self.request.user

        serializer: CreateProfileSerializer = CreateProfileSerializer(
            data = data
        )

        if not serializer.is_valid():

            response_data = json.dumps({
                'status': 'error',
                'message': 'Invalid request to API',
                'data': serializer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data: dict = serializer.validated_data
        town: str = validated_data.get('town')
        race: int = validated_data.get('race')
        gender: int = validated_data.get('gender')
        country: int = validated_data.get('country')
        province: int = validated_data.get('province')
        postal_code: int = validated_data.get('postal_code')
        street_address: str = validated_data.get('street_address')

        try:

            existing_profile = UserManagementPackage(
                user = user.id
            ).get_profile()

            if existing_profile:

                response_data = json.dumps({
                    'status': 'error', 
                    'message': 'Profile already exists for this user'
                })
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            UserManagementPackage(
                town = town,
                race = race,
                user = user.id,
                gender = gender,
                country = country,
                province = province,
                postal_code = postal_code,
                street_address = street_address
            ).create_profile()

            response_data = json.dumps({
                'status': 'success',
                'message': 'Profile is created successfully',
                'data': serializer.data
            })
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as message:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to create profile',
                'data': str(message)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def edit_profile(self):

        data = self.request.data
        user = self.request.user

        serializer: EditProfileSerializer = EditProfileSerializer(
            data = data
        )

        if not serializer.is_valid():

            response_data = json.dumps({
                'status': 'error',
                'message': 'Invalid request to API',
                'data': serializer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data: dict = serializer.validated_data
        town: str = validated_data.get('town')
        race: int = validated_data.get('race')
        gender: int = validated_data.get('gender')
        country: int = validated_data.get('country')
        province: int = validated_data.get('province')
        postal_code: int = validated_data.get('postal_code')
        street_address: str = validated_data.get('street_address')

        try:

            UserManagementPackage(
                town = town,
                race = race,
                user = user.id,
                gender = gender,
                country = country,
                province = province,
                postal_code = postal_code,
                street_address = street_address
            ).edit_profile()

            response_data = json.dumps({
                'status': 'success',
                'message': 'Profile is updated successfully',
                'data': serializer.data
            })
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as message:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to update profile',
                'data': str(message)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def view_profile(self):

        user = self.request.user

        profile = UserManagementPackage(
            user = user.id
        ).get_profile()

        try:

            model_serializer: ViewProfileModelSerializer = ViewProfileModelSerializer(
                profile,
                many = False
            )

            response_data = json.dumps({
                'status': 'success',
                'message': 'Profile is retrieved successfully',
                'data': model_serializer.data
            })
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as message:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to retrieve profile',
                'data': str(message)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def create_otp(self):

        user = self.request.user

        otp_code = self.generate_otp()
        expires_at = self.generate_time()

        one_time_pin = UserManagementPackage(
            user = user.id
        ).get_user_otp()

        if one_time_pin:

            one_time_pin.user = user
            one_time_pin.attempts = 0
            one_time_pin.is_used = False
            one_time_pin.otp_code = otp_code
            one_time_pin.expires_at = expires_at

            one_time_pin.save()

            response_data = json.dumps({
                'status': 'success',
                'message': 'One Time Pin is updated Successfully',
                'data': {
                    'one_time_pin': one_time_pin.otp_code,
                }
            })
            return Response(response_data, status=status.HTTP_201_CREATED)

        one_time_pin = UserManagementPackage(
            user = user.id,
            attempts = 0,
            is_used = False,
            otp_code = otp_code,
            expires_at = expires_at
        ).create_otp()

        response_data = json.dumps({
            'status': 'success',
            'message': 'One Time Pin is created Successfully',
            'data': {
                'one_time_pin': one_time_pin.otp_code,
            }
        })
        return Response(response_data, status=status.HTTP_201_CREATED)

    def send_otp(self):

        user = self.request.user

        user_otp = UserManagementPackage(
            user = user.id
        ).get_user_otp()

        try:

            html_tpl_path = "otp_email.html"
            receiver_email = [user.email]

            context_data = {
                "email": user.email,
                "last_name": user.last_name,
                "first_name": user.first_name,
                "otp_code": user_otp.otp_code,
                "login_url": self.global_frontend_url,
            }

            subject = f"Verification OTP - Spares"

            data_json = json.dumps({
                "html_tpl_path": html_tpl_path,
                "receiver_email": receiver_email,
                "context_data": context_data,
                "subject": subject,
            })

            thread = threading.Thread(target=send_email_api, args=(data_json,))
            thread.start()

            response_data = json.dumps({
                'status': 'success',
                'message': 'OTP sent successfull',
                'data': {
                    'one_time_pin': user_otp.otp_code,
                }
            })
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as message:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to send OTP',
                'data': str(message)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def create_user(self):

        data = self.request.data

        serializer: CreateUserSerializer = CreateUserSerializer(
            data = data
        )

        if not serializer.is_valid():

            response_data = json.dumps({
                'status': 'error',
                'message': 'Invalid request to API',
                'data': serializer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data: dict = serializer.validated_data
        role: str = validated_data.get('role')
        email: str = validated_data.get('email')
        last_name: str = validated_data.get('last_name')
        first_name: str = validated_data.get('first_name')
        phone_number: str = validated_data.get('phone_number')

        if not (email or phone_number):

            response_data = json.dumps({
                'status': 'error',
                'message': 'Please provide either email or phone number',
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        user_email = UserManagementPackage(
            email = email
        ).check_email()

        if user_email:

            response_data = json.dumps({
                'status': 'error',
                'message': 'The provided email already exist, please enter a different email'
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        user_phone_number = UserManagementPackage(
            phone_number = phone_number
        ).check_phone_number()

        if user_phone_number:

            response_data = json.dumps({
                'status': 'error',
                'message': 'The provided phone number already exist, please enter a different phone number'
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        password = self.generate_password()

        try:

            UserManagementPackage(
                email = email,
                role_id = role,
                password = password,
                last_name = last_name,
                first_name = first_name,
                phone_number = phone_number,
            ).create_user()

            response_data = json.dumps({
                'status': 'success',
                'message': 'User is created successfully',
                'data': serializer.data
            })
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as message:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to create a user, please try again',
                'data': str(message)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def edit_user(self):

        data = self.request.data

        serializer: EditUserSerializer = EditUserSerializer(
            data = data
        )

        if not serializer.is_valid():

            response_data = json.dumps({
                'status': 'error',
                'message': 'Invalid request to API',
                'data': serializer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data: dict = serializer.validated_data
        role: str = validated_data.get('role')
        email: str = validated_data.get('email')
        user_id: str = validated_data.get('user_id')
        last_name: str = validated_data.get('last_name')
        first_name: str = validated_data.get('first_name')
        phone_number: str = validated_data.get('phone_number')

        try:

            UserManagementPackage(
                email = email,
                role_id = role,
                user = user_id,
                last_name = last_name,
                first_name = first_name,
                phone_number = phone_number,
            ).edit_user()

            response_data = json.dumps({
                'status': 'success',
                'message': 'User is updated successfully',
                'data': serializer.data
            })
            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as message:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to update a user, please try again',
                'data': str(message)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def view_customer(self):

        user_package = UserManagementPackage(

        ).view_customer()

        model_serializer:ViewUserModelSerializer = ViewUserModelSerializer(
            user_package,
            many = True
        )

        response_data = json.dumps({
            'status': 'success',
            'message': 'Customers have been retrieved successfully',
            'data': model_serializer.data
        })
        return Response(response_data, status=status.HTTP_200_OK)

    def view_users(self):

        users = UserManagementPackage(

        ).view_users()

        model_serializer: ViewUserModelSerializer = ViewUserModelSerializer(
            users,
            many = True
        )

        response_data = json.dumps({
            'status': 'success',
            'message': 'Users retrived successfully',
            'data': model_serializer.data
        })
        return Response(response_data, status=status.HTTP_200_OK)

    def view_admin(self):

        user_package = UserManagementPackage(

        ).view_admin()

        model_serializer:ViewUserModelSerializer = ViewUserModelSerializer(
            user_package,
            many = True
        )

        response_data = json.dumps({
            'status': 'success',
            'message': 'Admin have been retrieved successfully',
            'data': model_serializer.data
        })
        return Response(response_data, status=status.HTTP_200_OK)

    def resend_otp(self):

        data = self.request.data

        serializer:ResendOTPSerializer = ResendOTPSerializer(
            data = data
        )

        if not serializer.is_valid():

            response_data = {
                'status': 'error',
                'message': 'Invalid request to API',
                'data': serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data: dict = serializer.validated_data
        username: str = validated_data.get('username')

        if not username:

            response_data = {
                'status': 'info',
                'message': 'Email or Phone number is required',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        try:

            if '@' in username:

                user = UserManagementPackage(
                    email = username
                ).get_user_email()

            else:

                user = UserManagementPackage(
                    phone_number = username
                ).get_user_phone_number()

        except Exception as message:

            response_data = {
                'status': 'error',
                'message': 'Failed to fetch user details',
                'data': str(message)
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        otp_code = self.generate_otp()
        expires_at = self.generate_time()

        one_time_pin = UserManagementPackage(
            user = user.id
        ).get_user_otp()

        if one_time_pin:

            one_time_pin.attempts = 0
            one_time_pin.is_used = False
            one_time_pin.otp_code = otp_code
            one_time_pin.expires_at = expires_at
            one_time_pin.save()

            response_data = {
                'status': 'success',
                'message': 'One Time Pin updated successfully',
                'data': {
                    'one_time_pin': one_time_pin.otp_code,
                }
            }

        else:

            one_time_pin = UserManagementPackage(
                user = user,
                attempts = 0,
                is_used = False,
                otp_code = otp_code,
                expires_at = expires_at
            ).create_otp()

            response_data = {
                'status': 'success',
                'message': 'One Time Pin created successfully',
                'data': {
                    'one_time_pin': one_time_pin.otp_code,
                }
            }

        return Response(response_data, status=status.HTTP_200_OK)

    def verify_otp(self):

        data = self.request.data
        user = self.request.user

        serializer: VerifyOTPSerializer = VerifyOTPSerializer(
            data = data
        )

        if not serializer.is_valid():

            response_data = {
                'status': 'error',
                'message': 'Invalid request to API',
                'data': serializer.errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data:dict = serializer.validated_data
        otp_code: int = validated_data.get('otp_code')

        otp_for_user = UserManagementPackage(
            user = user.id
        ).get_user_otp()

        if otp_for_user.is_used:

            response_data = {
                'status': 'error',
                'message': 'The provided OTP is already used, please request another OTP'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        current_time = timezone.now()

        if current_time > otp_for_user.expires_at:

            response_data = {
                'status': 'error',
                'message': 'The provided OTP is expired, please request another OTP'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if otp_for_user.attempts >= 5:

            response_data = {
                'status': 'error',
                'message': 'The provided OTP has reached the maximum attempts, please request another OTP'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if otp_for_user.otp_code != otp_code:

            otp_for_user.attempts += 1
            otp_for_user.save()

            response_data = {
                'status': 'error',
                'message': 'The provided OTP is invalid, please request another OTP'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        otp_for_user.is_used = True
        otp_for_user.save()

        response_data = {
            'status': 'success',
            'message': 'The provided OTP is verified successfully'
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def user_logout(self):

        user = self.request.user

        if not user.is_authenticated:

            response_data = json.dumps({
                'status': 'error',
                'message': 'The user is not logged in',
            })
            return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

        user_token_package = UserManagementPackage()

        user_token = user_token_package.create_token(
            user=user.id
        )
        user_token.delete()

        logout(self.request)

        response_data = json.dumps({
            'status': 'success',
            'message': 'User logged out successfully',
        })
        return Response(response_data, status=status.HTTP_200_OK)

    def reset_password(self):

        data = self.request.data

        serializer: ResetPasswordSerializer = ResetPasswordSerializer(
            data = data
        )

        if not serializer.is_valid():

            response_data = json.dumps({
                'status': 'error',
                'message': 'Invalid request to API',
                'data': serializer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data: dict = serializer.validated_data
        email: str = validated_data.get('email')
        password: str = validated_data.get('password')
        phone_number: str = validated_data.get('phone_number')

        if email:

            try:

                user = UserManagementPackage(
                    email=email
                ).get_user_email()

            except Exception as message:

                response_data = json.dumps({
                'status': 'error',
                'message': 'The provided email does not exist, please enter the correct email',
                'data': str(message)
                })
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        elif phone_number:

            try:

                user = UserManagementPackage(
                    email=email
                ).get_user_phone_number()

            except Exception as message:

                response_data = json.dumps({
                    'status': 'error',
                    'message': 'The provided phone number does not exist, please enter the correct phone number',
                    'data': str(message)
                })
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if user:

            user.set_password(password)
            user.save()

            response_data = json.dumps({
                'status': 'success',
                'message': 'Password is changed successfully',
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def forgot_password(self):

        data =  self.request.data

        serializer: ForgotPasswordSerializer = ForgotPasswordSerializer(
            data = data
        )

        if not serializer.is_valid():

            response_data = json.dumps({
                'status': 'error',
                'message': 'Invalid request to API',
                'data': serializer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data: dict = serializer.validated_data
        email: str = validated_data.get('email')
        phone_number: str = validated_data.get('phone_number')

        if email:

            try:

                UserManagementPackage(
                    email=email
                ).get_user_email()

                # Function to send an email
                response_data = json.dumps({
                'status': 'success',
                'message': 'Forgot password has been sent to the provided email',
                })
                return Response(response_data, status=status.HTTP_200_OK)

            except Exception as message:

                response_data = json.dumps({
                'status': 'error',
                'message': 'The provided email does not exist, please enter the correct email',
                'data': str(message)
                })
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        elif phone_number:

            try:

                UserManagementPackage(
                    email=email
                ).get_user_phone_number()

                # Function to send an email
                response_data = json.dumps({
                'status': 'success',
                'message': 'Forgot password has been sent to the provided email',
                })
                return Response(response_data, status=status.HTTP_200_OK)

            except Exception as message:

                response_data = json.dumps({
                    'status': 'error',
                    'message': 'The provided phone number does not exist, please enter the correct phone number',
                    'data': str(message)
                })
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def change_password(self):

        data = self.request.data
        user = self.request.user.id

        serializer: ChangePasswordSerializer = ChangePasswordSerializer(
            data = data
        )

        if not serializer.is_valid():

            response_data = json.dumps({
                'status': 'error',
                'message': 'Invalid request to API',
                'data': serializer.errors
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        validated_data: dict = serializer.validated_data
        old_password: str = validated_data.get('old_password')
        new_password: str = validated_data.get('new_password')
        confirm_password: str = validated_data.get('confirm_password')

        user = UserManagementPackage(
            user = user
        ).get_user()

        try:

            if not user.check_password(old_password):

                response_data = json.dumps({
                    'status': 'error',
                    'message': 'The provided old password does not match the active password, please try again',
                })
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            elif new_password != confirm_password:

                response_data = json.dumps({
                    'status': 'error',
                    'message': 'The provided new password and confirm password does not match, please try again',
                })
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            else:

                user.set_password(new_password)
                user.save()

                response_data = json.dumps({
                    'status': 'success',
                    'message': 'Password is changed successfully',
                })
                return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as message:

            response_data = json.dumps({
                'status': 'error',
                'message': 'Failed to Change the password, please try again',
                'data': str(message)
            })
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)













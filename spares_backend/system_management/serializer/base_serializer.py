from rest_framework import serializers


class SignUpSerializer(serializers.Serializer):

    email = serializers.CharField()
    password = serializers.CharField()
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    phone_number = serializers.IntegerField()


class LoginSerializer(serializers.Serializer):

    password = serializers.CharField(
        write_only=True,
    )
    email = serializers.EmailField(
        required=False,
        allow_null=True
    )
    phone_number = serializers.CharField(
        required=False,
        allow_null=True
    )


class CreateProfileSerializer(serializers.Serializer):

    town = serializers.CharField()
    race = serializers.IntegerField()
    gender = serializers.IntegerField()
    country = serializers.IntegerField()
    province = serializers.IntegerField()
    postal_code = serializers.IntegerField()
    street_address = serializers.CharField()


class EditProfileSerializer(serializers.Serializer):

    town = serializers.CharField()
    race = serializers.IntegerField()
    gender = serializers.IntegerField()
    country = serializers.IntegerField()
    province = serializers.IntegerField()
    postal_code = serializers.IntegerField()
    street_address = serializers.CharField()


class CreateUserSerializer(serializers.Serializer):

    email = serializers.EmailField(
        required=False,
        allow_null=True
    )
    last_name = serializers.CharField(
        max_length = 255
    )
    first_name = serializers.CharField(
        max_length = 255
    )
    role = serializers.CharField(
        max_length = 255
    )
    phone_number = serializers.CharField(
        required=False,
        allow_null=True
    )


class EditUserSerializer(serializers.Serializer):

    email = serializers.EmailField(
        required=False,
        allow_null=True
    )
    user_id = serializers.CharField(
        max_length = 255
    )
    last_name = serializers.CharField(
        max_length = 255
    )
    first_name = serializers.CharField(
        max_length = 255
    )
    role = serializers.CharField(
        max_length = 255
    )
    phone_number = serializers.CharField(
        required=False,
        allow_null=True
    )


class ResendOTPSerializer(serializers.Serializer):

    username = serializers.CharField(
        max_length = 255
    )


class VerifyOTPSerializer(serializers.Serializer):

    otp_code = serializers.CharField(
        max_length = 6
    )


class ResetPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(
        write_only=True,
    )
    email = serializers.EmailField(
        required=False,
        allow_null=True
    )
    phone_number = serializers.CharField(
        required=False,
        allow_null=True
    )


class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField(
        required=False,
        allow_null=True
    )
    phone_number = serializers.CharField(
        required=False,
        allow_null=True
    )


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(
        max_length = 255
    )
    new_password = serializers.CharField(
        max_length = 255
    )
    confirm_password = serializers.CharField(
        max_length = 255
    )





























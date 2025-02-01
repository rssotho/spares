from django.utils import timezone

from rest_framework.authtoken.models import Token

from system_management.models import (
    User,
    Role,
    Race,
    Gender,
    Country,
    Profile,
    Province,
    OneTimePin,
)
from global_app import constants as constant


class UserManagementPackage:

    def __init__(
        self,
        email: str = None,
        role_id: Role = None,
        password: int = None,
        last_name: str = None,
        first_name: str = None,
        phone_number: str = None,

        # OTP
        user: User = None,
        otp_code: int = None,
        is_used: bool = None,
        attempts: int = None,
        expires_at: timezone = None,

        # Profile
        race: Race = None,
        gender: Gender = None,
        country: Country = None,
        province: Province = None,

        town: str = None,
        postal_code: int = None,
        street_address: str = None

    ) -> None:

        # User
        self.user = user
        self.email = email
        self.role_id = role_id
        self.password = password
        self.last_name = last_name
        self.first_name = first_name
        self.phone_number = phone_number

        # OTP
        self.is_used = is_used
        self.otp_code = otp_code
        self.attempts = attempts
        self.expires_at = expires_at

        # Profle
        self.race = race
        self.gender = gender
        self.country = country
        self.province = province

        self.town = town
        self.postal_code = postal_code
        self.street_address = street_address

    def get_role(self) -> Role:

        role: Role = Role.objects.get(
            role = constant.CUSTOMER
        )

        if not role:

            raise ValueError('The provided role does not exist')

        return role

    def sign_up(self) -> User:

        sign_up = User.objects.create_user(
            email = self.email,
            role_id = self.role_id,
            password = self.password,
            last_name = self.last_name,
            first_name = self.first_name,
            phone_number = self.phone_number
        )

        if not sign_up:

            raise ValueError('Failed to create a user, please try again')

        return sign_up

    def user_login(self) -> User:

        if self.email:

            user: User = User.objects.filter(
                email=self.email
            ).first()

        elif self.phone_number:

            user: User = User.objects.filter(
                phone_number=self.phone_number
            ).first()

        if not user:

            raise ValueError('Invalid Email or Phone Number')

        return user

    def create_token(self, user: User) -> Token:

        token, _ = Token.objects.get_or_create(
            user=user
        )

        if token is None:

            raise ValueError('The requesting user does not have the token')

        return token

    def get_user(self) -> User:

        user: User = User.objects.get(
            id = self.user
            )

        if not user:

            raise ValueError('User does not exist')

        return user

    def get_user_otp(self) -> OneTimePin:

        user = self.get_user()

        try:

            otp_user = OneTimePin.objects.get(
                user = user
            )

            return otp_user

        except OneTimePin.DoesNotExist:

            return None

    def create_otp(self) -> OneTimePin:

        user = self.get_user()

        one_time_pin: OneTimePin = OneTimePin.objects.create(
            user = user,
            is_used = False,
            otp_code = self.otp_code,
            attempts = self.attempts,
            expires_at = self.expires_at,
            date_created = timezone.now()
        )

        return one_time_pin

    def get_race(self) -> Race:

        race = Race.objects.get(
            id = self.race
        )

        if race is None:

            raise ValueError ('Race does not exist')

        return race

    def get_gender(self) -> Gender:

        gender = Gender.objects.get(
            id = self.gender
        )

        if gender is None:

            raise ValueError ('Gender does not exist')

        return gender

    def get_country(self) -> Country:

        country: Country = Country.objects.get(
            id = self.country
        )

        if not country:

            raise ValueError ('Country does not exist')

        return country

    def get_province(self) -> Province:

        province = Province.objects.get(
            id = self.province
        )

        if province is None:

            raise ValueError ('Province does not exist')

        return province

    def create_profile(self) -> Profile:

        race = self.get_race()
        user = self.get_user()
        gender = self.get_gender()
        country = self.get_country()
        province = self.get_province()

        profile = Profile.objects.create(
            user = user,
            race = race,
            gender = gender,
            town = self.town,
            country = country,
            province = province,
            postal_code = self.postal_code,
            street_address = self.street_address,
        )

        if not profile:

            raise ValueError('Failed to create profile, please try again')

        return profile

    def get_profile(self) -> Profile:

        user = self.get_user()

        profile: Profile = Profile.objects.get(
            user_id = user
        )

        if not profile:

            raise ValueError('User does not have profile')

        return profile

    def edit_profile(self) -> Profile:

        race = self.get_race()
        user = self.get_profile()
        gender = self.get_gender()
        country = self.get_country()
        province = self.get_province()

        user.race = race
        user.gender = gender
        user.town = self.town
        user.country = country
        user.province = province
        user.postal_code = self.postal_code
        user.street_address = self.street_address

        user.save()

        return user

    def create_user(self) -> User:

        role = self.get_roles()

        user_details = User.objects.create_user(
            role_id = role.id,
            password = self.password,
            email = self.email or None,
            last_name = self.last_name,
            first_name = self.first_name,
            phone_number = self.phone_number or None,
        )

        if not user_details:

            raise ValueError ('Failed to create user')

        return user_details

    def edit_user(self) -> User:

        user = self.get_user()
        role = self.get_roles()

        user.role = role
        user.email = self.email
        user.last_name = self.last_name
        user.first_name = self.first_name
        user.phone_number = self.phone_number

        user.save()

        return user

    def check_email(self) -> User:

        user_email: User = User.objects.filter(
            email = self.email
        ).exists()

        return user_email

    def check_phone_number(self) -> User:

        user_phone_number: User = User.objects.filter(
            phone_number = self.phone_number
        ).exists()

        return user_phone_number

    def filter_customer_role(self) -> Role:

        user_role: Role = Role.objects.get(
            role = constant.CUSTOMER
        )

        return user_role

    def filter_admin_role(self) -> Role:

        user_role: Role = Role.objects.get(
            role = constant.SYSTEM_ADMIN
        )

        return user_role

    def view_customer(self) -> User:

        role = self.filter_customer_role()

        user:User = User.objects.filter(
            role_id = role
        ).all()

        return user

    def view_users(self) -> User:

        users: User = User.objects.all()

        return users

    def view_admin(self) -> User:

        role = self.filter_admin_role()

        user:User = User.objects.filter(
            role_id = role
        ).all()

        return user

    def get_user_email(self) -> User:

        user: User = User.objects.filter(
            email = self.email
        ).first()

        if user is None:

            raise ValueError ('User with the provide email does not exist, please enter a correct email')

        return user

    def get_user_phone_number(self) -> User:

        user: User = User.objects.filter(
            phone_number = self.phone_number
        ).first()

        if user is None:

            raise ValueError ('User with the provide phone number does not exist, please enter a correct phone number')

        return user

    def get_roles(self) -> Role:

        try:

            role: Role = Role.objects.get(
                id = self.role_id
            )

            return role

        except Role.DoesNotExist:

            raise ValueError ('Role does not exist')


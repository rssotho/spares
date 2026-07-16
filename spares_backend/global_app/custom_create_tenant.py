from client.models import client
from django_tenants.utils import schema_context
from django.core.management.base import BaseCommand

from system_management.models import (
    User
)

class Command(BaseCommand):
    help = 'Create a superuser for a specific tenant with custom options'

    def get_valid_input(self, prompt, error_message):

        while True:

            user_input = input(prompt)

            if user_input:

                return user_input

            else:

                self.stdout.write(self.style.ERROR(error_message))

    def handle(self, *args, **options):

        tenant = None

        while not tenant:

            tenant_schema_name = self.get_valid_input(
                'Tenant schema name: ',
                'Please provide the tenant schema name.'
            )

            try:

                tenant: client = client.objects.get(
                    schema_name = tenant_schema_name
                )

            except client.DoesNotExist:

                self.stdout.write(
                    self.style.ERROR
                    (f'Tenant "{tenant_schema_name}" does not exist.')
                    )
                tenant=None

        # Switch to the tenant schema context
        with schema_context(tenant.schema_name):

            email_address = None

            while not email_address:

                email_address = self.get_valid_input(
                    'Email address: ',
                    'Please provide an email address.'
                )

                email_exists: User = User.objects.filter(
                    email = email_address
                ).exists()

                if email_exists:

                    self.stdout.write(self.style.ERROR('Email already exists'))
                    email_address = None

            first_name = self.get_valid_input(
                'First Name: ',
                'Please provide first name.'
            )

            last_name = self.get_valid_input(
                'Last Name: ',
                'Please provide last name.'
            )

            phone_number = None

            while not phone_number:

                phone_number = self.get_valid_input(
                    'Phone number: ',
                    'Please provide a phone number.'
                )

                if not phone_number.isdigit():

                    self.stdout.write(self.style.ERROR('Phone number must be a number.'))
                    phone_number = None

                    continue

                phone_number_exists: User = User.objects.filter(
                    phone_number = phone_number
                ).exists()

                if phone_number_exists:

                    self.stdout.write(self.style.ERROR('Phone number already exists'))
                    phone_number = None

            password = self.get_valid_input(
                'Password: ',
                'Please provide a password.'
            )

            confirm_password = self.get_valid_input(
                'Confirm password: ',
                'Please confirm your password.'
            )

            while password != confirm_password:

                self.stdout.write(self.style.ERROR('Passwords do not match.'))

                password = self.get_valid_input(
                    'Password: ',
                    'Please provide a password.'
                )

                confirm_password = self.get_valid_input(
                    'Confirm password: ',
                    'Please confirm your password.'
                )

            # Create the superuser and related objects
            User.objects.create_superuser(
                password = password,
                email = email_address,
                last_name = last_name,
                first_name = first_name,
                phone_number = phone_number,
            )

            self.stdout.write(self.style.SUCCESS(f'Tenant superuser created successfully for "{tenant_schema_name}"!'))
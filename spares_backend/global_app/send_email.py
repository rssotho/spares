"""
Handle the email sending services required by the web application.
"""
import json

import boto3
from decouple import config
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template.loader import render_to_string
from rest_framework import serializers

from global_app.classes import (
    BaseFormSerializer
)


class SendEmailSerializer(BaseFormSerializer):
    """Send email post data validation and cleaning"""
    context_data = serializers.DictField(
        allow_empty=True,
        required=False
    )
    html_tpl_path = serializers.CharField(
        max_length=100,
        required=True
    )
    subject = serializers.CharField(
        max_length=100,
        required=True
    )
    receiver_email = serializers.ListSerializer(
        child=serializers.CharField(
            max_length=100,
            required=True
        )
    )


def send_email_api(data):
    """
    Problem:
        Sending email notification to the users via API call

    Solution:
        Use Sendgrid to send a email to the user email.

    Args:
        data: Dictionary data for email sending

    Logic:
        1. Extract data from the request data.
        2. Serialize the data.
        3. If the data is invalid:
            - Create an error response with a message indicating an invalid request.
            - Return a 400 Bad Request response with the error data.
        4. Otherwise, extract the following fields from the serialized data:
            - html_tpl_path
            - context_data
            - subject
        5. Render the html template with the context data.
        6. Send the email to the user email.
        7. Return a success response with the serialized data.
        8. If an error occurs during the email sending process:
            - Create an error response with a message indicating an error occurred.
            - Return a 500 Internal Server Error response with the error data.
    
    Return:
        Response: A JSON serialized response 
            400-Bad request : if there is a issue with the request sent to the api.
            200-OK : if the email was sent successfully.
            500-Internal Server Error : if the email sending process failed.
    
    Raises:
        Exception: If an error occurs during the email sending process.
    
    """
    data = json.loads(data)
    serializer = SendEmailSerializer(data=data)

    if serializer.is_valid():
        html_tpl_path = serializer.validated_data['html_tpl_path']
        context_data = serializer.validated_data['context_data']
        subject = serializer.validated_data['subject']

        try:
            receiver_email = serializer.validated_data['receiver_email']
        except Exception as error_message:
            raise ValueError(f'{error_message}')

        try:

            html_tpl_path = f"{config('DOMAIN')}_emails/{html_tpl_path}"
            context_data = context_data
            receiver_emails = receiver_email if isinstance(receiver_email, list) else [
                receiver_email
            ]

            email_html_template = get_template(html_tpl_path).render(context_data)

            email_msg = EmailMessage(
                subject,
                email_html_template,
                settings.FROM_EMAIL,
                receiver_emails,
                reply_to=[settings.FROM_EMAIL]
            )

            email_msg.content_subtype = 'html'
            email_msg.send(fail_silently=False)

        except Exception as error_message:
            raise ValueError(f'{error_message}')

    else:
        raise ValueError(f'{serializer.errors}')

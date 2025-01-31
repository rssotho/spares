from rest_framework import serializers

from system_management.models import (
    User,
    Profile,
)


class ViewProfileModelSerializer(serializers.Serializer):

    class Meta:
        model = Profile
        fields = (
            'id',
            'town',
            'race',
            'gender',
            'country',
            'province',
            'postal_code',
            'street_address',
        )


class ViewUserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'role',
            'email',
            'last_name',
            'first_name',
            'phone_number',
        )











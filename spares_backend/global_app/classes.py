"""
Global classes for all apps.
"""
from rest_framework import serializers


class BaseFormSerializer(serializers.Serializer):
    """Base form serializer for cleaning incoming and outgoing data"""

    def create(self, validated_data):
        """Override create method to do nothing"""

    def update(self, instance, validated_data):
        """Override create method to do nothing"""

    def is_model_instance_exists(self, instance_id, instance):
        """
        Check if a model instance with the given ID exists.

        Args:
            instance_id (int): The ID of the model instance to check.
            instance (models.Model): The model class to query.

        Returns:
            bool: True if the instance exists, False otherwise.
        """
        try:
            instance.objects.get(id=instance_id)
            return True
        except instance.DoesNotExist:
            return False


class BaseModelSerializer(serializers.ModelSerializer):
    """Base model serializer for pylint public functions"""

    def create(self, validated_data):
        """Override create method to do nothing"""

    def update(self, instance, validated_data):
        """Override create method to do nothing"""

    class Meta:
        """Meta class for base model serializer."""

        def get_field_names(self):
            """Return a list of field names."""
            return super()

        def get_extra_kwargs(self):
            """Return a dictionary of extra keyword arguments."""
            return super()

# Generated by Django 5.1.4 on 2025-01-03 09:55

from django.db import migrations

from global_app.constants import (
    GAUTENG,
    LIMPOPO,
    FREE_STATE,
    MPUMALANGA,
    NORTH_WEST,
    WESTERN_CAPE,
    EASTERN_CAPE,
    NORTHERN_CAPE,
    KWAZULU_NATAL
)


def create_provice(apps, schema_editor):

    Province = apps.get_model('system_management', 'Province')
    Province.objects.bulk_create([
        Province(province=GAUTENG),
        Province(province=LIMPOPO),
        Province(province=FREE_STATE),
        Province(province=MPUMALANGA),
        Province(province=NORTH_WEST),
        Province(province=WESTERN_CAPE),
        Province(province=EASTERN_CAPE),
        Province(province=NORTHERN_CAPE),
        Province(province=KWAZULU_NATAL)
    ])


class Migration(migrations.Migration):


    dependencies = [
        ('system_management', '0003_auto_20250103_1151'),
    ]

    operations = [
        migrations.RunPython(create_provice),
    ]

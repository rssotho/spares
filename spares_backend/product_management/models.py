from django.db import models

from system_management.models import User


class Category(models.Model):

    category_name = models.CharField(
        max_length = 255
    )
    description = models.CharField(
        blank = True
    )
    date_created = models.DateTimeField(
        auto_now_add = True
    )
    date_modified = models.DateTimeField(
        auto_now_add = True
    )
    user = models.ForeignKey(
        User,
        on_delete = models.PROTECT
    )


class CategoryProfile(models.Model):

    file_url = models.URLField(
        blank = True
    )
    date_created = models.DateTimeField(
        auto_now_add = True
    )
    date_modified = models.DateTimeField(
        auto_now_add = True
    )
    category = models.ForeignKey(
        Category,
        on_delete = models.PROTECT
    )


class Product(models.Model):

    product_name = models.CharField(
        max_length = 255
    )
    description = models.CharField(
        max_length = 255
    )
    total_items = models.IntegerField()
    price = models.FloatField()
    date_created = models.DateTimeField(
        auto_now_add = True
    )
    date_modified = models.DateTimeField(
        auto_now_add = True
    )
    category = models.ForeignKey(
        Category,
        on_delete = models.PROTECT
    )
    user = models.ForeignKey(
        User,
        on_delete = models.PROTECT
    )


class ProductProfile(models.Model):

    file_url = models.URLField()
    date_created = models.DateTimeField(
        auto_now_add = True
    )
    date_modified = models.DateTimeField(
        auto_now_add = True
    )
    product = models.ForeignKey(
        Product,
        on_delete = models.PROTECT
    )













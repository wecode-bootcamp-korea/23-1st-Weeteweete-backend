from typing import Mapping
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "products"


class Category(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    name    = models.CharField(max_length=100)

    class Meta:
        db_table = "categories"


class Concept(models.Model):
    name     = models.CharField(max_length=100)
    content  = models.TextField(default='')

    class Meta:
        db_table = "concepts"    


class Item(models.Model):
    concept        = models.ForeignKey("Concept", on_delete=models.CASCADE)
    color          = models.ForeignKey("Color", on_delete=models.CASCADE, null=True)
    option         = models.ForeignKey("Option", on_delete=models.CASCADE, null=True)
    category       = models.ForeignKey("Category", on_delete=models.CASCADE)
    name           = models.CharField(max_length=100)
    price          = models.DecimalField(max_digits=10, decimal_places=2)
    discount       = models.DecimalField(max_digits=10, decimal_places=2)
    stock          = models.IntegerField()
    order_quantity = models.IntegerField(default=0)

    class Meta:
        db_table = "items"


class Color(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "colors"  


class Option(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "options"  


class Image(models.Model):
    item      = models.ForeignKey("Item", on_delete=models.CASCADE)
    image_url = models.CharField(max_length=500)
    main      = models.BooleanField(default=False)

    class Meta:
        db_table = "images"  


class Review(models.Model):
    member    = models.ForeignKey("users.Member", on_delete=models.CASCADE)
    item      = models.ForeignKey("products.Item", on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    image_url = models.ImageField(upload_to="images", null=True)
    content   = models.TextField()
    grade     = models.IntegerField()

    
    class Meta:
        db_table = "reviews"
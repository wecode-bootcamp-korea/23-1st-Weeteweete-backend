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
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    name     = models.CharField(max_length=100)

    class Meta:
        db_table = "concepts"    


class Item(models.Model):
    concept  = models.ForeignKey("Concept", on_delete=models.CASCADE)
    color    = models.ForeignKey("Color", on_delete=models.CASCADE)
    option   = models.ForeignKey("Option", on_delete=models.CASCADE)
    image    = models.ForeignKey("Image", on_delete=models.CASCADE)
    name     = models.CharField(max_length=100)
    price    = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    stock    = models.IntegerField()

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
    image_url = models.CharField(max_length=500)

    class Meta:
        db_table = "images"  

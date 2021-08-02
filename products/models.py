from _typeshed import Self
from django.db import models
from django.db.models.deletion import SET_NULL

class Product(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = "products"


class Category(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    name    = models.CharField(max_length=45)

    class Meta:
        db_table = "categories"


class Item(models.Model):
    category       = models.ForeignKey("Category", on_delete=models.CASCADE)
    name           = models.CharField(max_length=100)
    fake_price     = models.IntegerField()
    real_price     = models.IntegerField()
    count          = models.IntegerField()
    option         = models.CharField(max_length=100)
    color          = models.CharField(max_length=45, null=True)
    planner_option =  models.CharField(max_length=45, null=True)
    new            = models.BooleanField()

    class Meta:
        db_table = "items"


class Review(models.Model):
    member     = models.ForeignKey("users.Member", on_delete=models.CASCADE)
    item       = models.ForeignKey("Item", on_delete=models.CASCADE)
    comment    =  models.ForeignKey("self", on_delete=SET_NULL, related_name="comment")
    created_at = models.DateTimeField(auto_now_add=True)
    image_url  = models.CharField(max_length=500, null=True)
    content    = models.TextField()

    class Meta:
        db_table = "reviews"

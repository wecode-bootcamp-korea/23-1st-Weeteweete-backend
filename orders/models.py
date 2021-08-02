from django.db import models
from django.db.models.deletion import CASCADE

class Order(models.Model):
    member = models.ForeignKey("users.Member", on_delete=models.CASCADE)
    item =  models.ForeignKey("products.Item", on_delete=models.CASCADE)
    count =  models.IntegerField()
    order_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "orders"

    
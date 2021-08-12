from django.db import models

class Member(models.Model):
    account       = models.CharField(max_length=45, unique=True)
    password      = models.CharField(max_length=500)
    name          = models.CharField(max_length=50)
    phone_number  = models.CharField(max_length=200)
    email         = models.CharField(max_length=200)
    points        = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    address       = models.CharField(max_length=500)
    
    class Meta:
        db_table = "members"


class Wish(models.Model):
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    item   = models.ForeignKey("products.Item", on_delete=models.CASCADE)

    class Meta:
        db_table = "wishes"  



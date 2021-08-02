from django.db import models

class Member(models.Model):
    login_id  = models.CharField(max_length=45, unique=True)
    password  = models.CharField(max_length=500)
    name      = models.CharField(max_length=50)
    address   = models.CharField(max_length=500)
    cellphone = models.CharField(max_length=200)
    email     = models.CharField(max_length=200)
    points    = models.IntegerField(null=True)

    class Meta:
        db_table = "members"




class NonMember(models.Model):
    order     = models.ForeignKey("orders.Oreder", on_delete=models.CASCADE)
    password  = models.CharField(max_length=500)
    name      = models.CharField(max_length=50)
    address   = models.CharField(max_length=500)
    cellphone = models.CharField(max_length=200)
    email     = models.CharField(max_length=200)

    class Meta:
        db_table = "nonmembers"




class Cart(models.Model):
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    item   = models.ForeignKey("products.Item", on_delete=models.CASCADE)
    count  = models.IntegerField()

    class Meta:
        db_table = "carts"  


class Wish(models.Model):
    member = models.ForeignKey("Member", on_delete=models.CASCADE)
    item   = models.ForeignKey("products.Item", on_delete=models.CASCADE)

    class Meta:
        db_table = "wishes"  
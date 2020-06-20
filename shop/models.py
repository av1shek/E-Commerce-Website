from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=75, default="")
    price = models.IntegerField(default=0)
    tagline = models.CharField(max_length=100, default="")
    desc = models.CharField(max_length=2000, default="")
    # No. of quantities for each color and size
    sblack = models.IntegerField(default=1)
    mblack = models.IntegerField(default=1)
    lblack = models.IntegerField(default=1)
    xlblack = models.IntegerField(default=1)

    sblue = models.IntegerField(default=1)
    mblue = models.IntegerField(default=1)
    lblue = models.IntegerField(default=1)
    xlblue = models.IntegerField(default=1)

    image = models.ImageField(upload_to="shop/themes/images", default="")                      #### check it should be media folder
    subimg1 = models.ImageField(upload_to="shop/themes/images", default="")
    subimg2 = models.ImageField(upload_to="shop/themes/images", default="")
    subimg3 = models.ImageField(upload_to="shop/themes/images", default="")
    subimg4 = models.ImageField(upload_to="shop/themes/images", default="")

    def __str__(self):
        return self.product_name


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=4000)
    fname = models.CharField(max_length=90)
    lname = models.CharField(max_length=90)
    amount = models.IntegerField(default=0)
    branch = models.CharField(max_length=90)
    reg_id = models.CharField(max_length=90)
    mobno = models.CharField(max_length=90)
    email = models.CharField(max_length=90)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    comment = models.CharField(max_length=1000)

class Message(models.Model):
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=90)
    message = models.CharField(max_length=1000)

    def __str__(self):
        title = self.name + "(" + self.email + ")"
        return title

class OrderStatus(models.Model):
    orderid = models.CharField(max_length=1000, default="")
    orderstatus = models.CharField(max_length=1000)
from django.db import models
from django.conf import settings
# Create your models here.

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=200)

    def __str__(self):
        return self.brand_name


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    img_one = models.ImageField(upload_to='media/')
    img_two = models.ImageField(upload_to='media/',null=True ,blank=True)
    img_three = models.ImageField(upload_to='media/',null=True ,blank=True)
    img_four = models.ImageField(upload_to='media/',null=True ,blank=True)
    img_five = models.ImageField(upload_to='media/',null=True ,blank=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    discription = models.TextField(max_length=500)
    price = models.IntegerField()
    discoutn_price = models.IntegerField()


    def __str__(self):
        return self.title

    def item_price(self):
        return self.price


    def item_discount(self):
        data = (self.item_price() * self.discoutn_price)/100
        return self.item_price() - data


class CartItem(models.Model):
    cart_id = models.AutoField(primary_key=True)
    itme = models.ForeignKey(Item,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    qty = models.IntegerField(default=1)


    def get_total_price(self):
        return self.qty * self.itme.price


    def get_discount_price(self):
        data = (self.get_total_price() * self.itme.discoutn_price)/100
        return self.get_total_price() - data


    def final_price(self):
        if self.itme.discoutn_price:
            return self.get_discount_price()
        else:
            return self.get_total_price()



class UserAddress(models.Model):
    address_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    contact = models.IntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    alternative_no = models.CharField(max_length=200)



class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    ordered = models.BooleanField(default=False)
    order_date = models.DateTimeField(null=True)
    add_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    address = models.ForeignKey(UserAddress,on_delete=models.CASCADE,blank=True,null=True)


    def get_total(self):
        total = 0
        for x in self.items.all():
            total += x.final_price()
        return total


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    amount = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)

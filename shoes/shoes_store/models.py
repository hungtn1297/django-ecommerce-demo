from django.db import models


# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.TextField()

    def __str__(self):
        return self.name


class Shoes(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    image = models.TextField()
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user_name = models.CharField(max_length=255, default='')
    full_name = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=255, default='')


class Cart(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Shoes, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    # def __str__(self):
    #     return "Cart: " + str(self.cart_id.id) + " - User: " + str(self.cart_id.user_id.user_name)  + " - Item: " + self.item_id.name


class Order(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=10, default='')
    email = models.EmailField(default='')
    address= models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    item_id = models.ForeignKey(Shoes, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()


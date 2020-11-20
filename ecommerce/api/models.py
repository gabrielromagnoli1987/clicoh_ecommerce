from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum


class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.FloatField()

    def __str__(self):
        return 'Name: {}, Price: {}'.format(self.name, self.price)


class Order(models.Model):
    date_time = models.DateTimeField(auto_now=True)

    def get_total(self):
        return self.order_details.aggregate(Sum('price'))['price__sum']

    def __str__(self):
        return 'id: {}'.format(self.id)


class OrderDetail(models.Model):
    product = models.ForeignKey(Product, related_name='order_detail', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.FloatField()
    order = models.ForeignKey(Order, related_name='order_details', on_delete=models.CASCADE)

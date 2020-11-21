from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ecommerce.api.models import Product, Order, OrderDetail


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ['id', 'quantity', 'price', 'product', 'order']
        read_only_fields = ['price']

    def create(self, validated_data):
        product = validated_data['product']
        order = validated_data['order']
        quantity = validated_data['quantity']
        price = product.price * quantity
        order_detail = OrderDetail()
        order_detail.price = price
        order_detail.quantity = quantity
        order_detail.product = product
        order_detail.order = order
        order_detail.save()
        return order_detail

    def update(self, instance, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']
        price = product.price * quantity
        instance.quantity = quantity
        instance.price = price
        instance.save()
        return instance

    def validate(self, data):
        # this validation runs automatically before the create or update method
        product = data['product']
        order = data['order']

        # if editing (put/patch method will be called)
        if self.instance:
            if self.instance.product.id != product.id or self.instance.order.id != order.id:
                raise ValidationError('You can only change the quantity')
        else:
            # create method will be called
            # validates that the product doesn't already exists on another orderDetail of the same order
            if OrderDetail.objects.filter(product=product.id, order=order.id).exists():
                raise ValidationError('That product already exists in the order')
        return data


class OrderSerializer(serializers.ModelSerializer):
    order_details = OrderDetailSerializer(many=True, read_only=True)
    total = serializers.FloatField(source='get_total', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'date_time', 'order_details', 'total']

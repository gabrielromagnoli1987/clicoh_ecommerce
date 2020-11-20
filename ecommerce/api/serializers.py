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

    def validate(self, data):
        # this validation runs automatically before the create method
        # validates that the product doesn't already exists on another orderDetail of the same order
        product = data['product']
        order = data['order']
        if OrderDetail.objects.filter(product=product.id, order=order.id).exists():
            raise ValidationError('That product already exists in the order')
        return data


class OrderSerializer(serializers.ModelSerializer):
    order_details = OrderDetailSerializer(many=True, read_only=True)
    total = serializers.FloatField(source='get_total', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'date_time', 'order_details', 'total']

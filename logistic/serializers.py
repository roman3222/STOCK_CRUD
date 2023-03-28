from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']




class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']




class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    class Meta:
        model = Stock
        fields = ['address', 'positions']


    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)

        for position in positions:
            StockProduct.objects.create(
                product=position['product'],
                quantity=position.get('quantity', 1),
                price=position.get('price', 0)
            )
        return stock

    def update(self, instance, validated_data):
        positions_data = validated_data.pop('positions', [])
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        for position_data in positions_data:
            product = position_data.get('product')
            if product is None:
                continue

            position, created = StockProduct.objects.get_or_create(
                stock=instance,
                product=product,
            )

            position.quantity = position_data.get('quantity', position.quantity)
            position.price = position_data.get('price', position.price)

        return instance




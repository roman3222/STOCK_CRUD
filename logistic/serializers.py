from rest_framework import serializers

from logistic.models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']




class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['quantity', 'price']




class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    class Meta:
        model = Stock
        fields = '__all__'


    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)

        for position in positions:
            StockProduct.objects.create(
                product=position['product'],
                quantity=position.get('quantuty', 1),
                price=position.get('price', 0)
            )
        return stock

    def update(self, instance, validated_data):
        positions_data = validated_data.pop('positions')
        positions = {pos['product'].id: pos for pos in positions_data}

        for sp in instance.positions.all():
            pos = positions.pop(sp.product.id, None)
            if pos:
                sp.quantity = pos.get('quantity', sp.quantity)
                sp.price = pos.get('price', sp.price)
                sp.save()

        for pos in positions.values():
            StockProduct.objects.create(
                product=pos['product'],
                quantity=pos.get('quantity', 1),
                price=pos.get('price', 0)

            )

        instance.title = validated_data.get('name', instance.title)
        instance.description = validated_data.get('description', instance.description)

        return instance



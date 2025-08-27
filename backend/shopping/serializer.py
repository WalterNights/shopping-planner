from .models import *
from rest_framework import serializers

class SupermarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supermarket
        fields = ['id', 'name', 'url', 'logo']
        
    def create(self, validated_data):
        supermarket, created = Supermarket.objects.get_or_create(**validated_data)
        return supermarket
    
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'logo']
        
    def create(self, validated_data):
        brand, created = Brand.objects.get_or_create(**validated_data)
        return brand
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        
    def create(self, validated_data):
        category, created = Category.objects.get_or_create(**validated_data)
        return category
    
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_id']
        
    def create(self, validated_data):
        product, created = Product.objects.get_or_create(**validated_data)
        return product
    
class ProductVariantSerializer(serializers.ModelSerializer):
    supermarket = SupermarketSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    supermarket_id = serializers.PrimaryKeyRelatedField(queryset=Supermarket.objects.all(), source='supermarket', write_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), source='brand', write_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    
    class Meta:
        model = ProductVariant
        fields = ['id', 'supermarket', 'supermarket_id', 'brand', 'brand_id', 'product', 'product_id', 'price', 'last_updated']
        
    def create(self, validated_data):
        productVariant, created = ProductVariant.objects.get_or_create(**validated_data)
        return productVariant
    
class HistoryPriceSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)
    product_variant_id = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all(), source='product_variant', write_only=True)
    
    class Meta:
        model = HistoryPrice
        fields = ['id', 'product_variant', 'product_variant_id', 'price', 'recorded_at']
        
    def create(self, validated_data):
        return super().create(validated_data)
    
class ShoppingListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    supermarket = SupermarketSerializer(read_only=True)
    supermarket_id = serializers.PrimaryKeyRelatedField(queryset=Supermarket.objects.all(), source='supermarket', write_only=True)
    
    class Meta:
        model = ShoppingList
        fields = ['id', 'user', 'supermarket', 'supermarket_id', 'created_at', 'updated_at']
        
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
    
class ShoppingItemSerializer(serializers.ModelSerializer):
    list = ShoppingListSerializer(read_only=True)
    product_variant = ProductVariantSerializer(read_only=True)
    list_id = serializers.PrimaryKeyRelatedField(queryset=ShoppingList.objects.all(), source='list', write_only=True)
    product_variant_id = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all(), source='product_variant', write_only=True)
    
    class Meta:
        model = ShoppingItem
        fields = ['id', 'list', 'list_id', 'product_variant', 'product_variant_id', 'quantity']
        
    def create(self, validated_data):
        return super().create(validated_data)
    
class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = ShoppingCart
        fields = ['id', 'user', 'created_at', 'updated_at']
        
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
    
class CartItemSerializer(serializers.ModelSerializer):
    cart = ShoppingCartSerializer(read_only=True)
    product = ProductVariantSerializer(read_only=True)
    cart_id = serializers.PrimaryKeyRelatedField(queryset=ShoppingCart.objects.all(), source='cart', write_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all(), source='product', write_only=True)
    
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'cart_id', 'product', 'product_id', 'quantity', 'subtotal']
        
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.subtotal = validated_data.get('subtotal', instance.subtotal)
        instance.save()
        return instance
    
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'total_amount', 'status', 'created_at', 'updated_at']
        
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.save()
        return instance
    
class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    product = ProductVariantSerializer(read_only=True)
    order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), source='order', write_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all(), source='product', write_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'order_id', 'product', 'product_id', 'quantity', 'price']
        
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance
    
class PaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), source='order', write_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'order', 'order_id', 'amount', 'payment_method', 'status', 'transaction_id', 'created_at']
        
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.transaction_id = validated_data.get('transaction_id', instance.transaction_id)
        instance.save()
        return instance
    
class PurchaseSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    product_variant = ProductVariantSerializer(read_only=True)
    product_variant_id = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all(), source='product_variant', write_only=True)
    
    class Meta:
        model = Purchase
        fields = ['id', 'user', 'product_variant', 'product_variant_id', 'quantity', 'total_price', 'purchase_date']
        
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
    
class PurchaseItemSerializer(serializers.ModelSerializer):
    purchase = PurchaseSerializer(read_only=True)
    product = ProductVariantSerializer(read_only=True)
    purchase_id = serializers.PrimaryKeyRelatedField(queryset=Purchase.objects.all(), source='purchase', write_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all(), source='product', write_only=True)
    
    class Meta:
        model = PurchaseItem
        fields = ['id', 'purchase', 'purchase_id', 'product', 'product_id', 'quantity', 'price']
        
    def create(self, validated_data):
        return super().create(validated_data)
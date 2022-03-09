from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image']

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'BasketID', 'DateTimeOrdered', 'UserID']

class BasketItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ['id', 'product_name', 'Quantity', 'price']


class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemsSerializer(many=True, read_only=True, source='basketitems_set')

    class Meta:
        model = Basket
        fields = ['id', 'UserID', 'is_active', 'items']

class APIUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = APIUser
        fields = ['id', 'email', 'username']

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']
        password = validated_data['password'] # Extract the username, email and passwor from the serializer
        new_user = APIUser.objects.create_user(username=username, email=email, password=password) # Create a new APIUser
        new_user.save() # Save the new user
        return new_user

class AddBasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ['ProductID']
    
    def create(self, validated_data):
        ProductID = validated_data['ProductID']
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            shopping_basket = Basket.objects.filter(UserID=current_user, is_active=True).first()
            if shopping_basket is None:
                Basket.objects.create(UserID = current_user)
                shopping_basket = Basket.objects.filter(UserID=current_user, is_active=True).first()
            # Check if the item is already in the basket
            basket_items = BasketItem.objects.filter(ProductID=ProductID, BasketID=shopping_basket).first()
            if basket_items:
                basket_items.Quantity = basket_items.Quantity + 1 # if it is already in the basket, add to the quantity
                basket_items.save()
                return basket_items
            else:
                new_basket_item = BasketItem.objects.create(BasketID=shopping_basket, ProductID=ProductID)
                return new_basket_item
            
        else:
            return None

class RemoveBasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ['ProductID']


    def create(self, validated_data):
        ProductID = validated_data['ProductID']
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            shopping_basket = Basket.objects.filter(UserID=current_user, is_active=True).first()
            # Check if the item is already in the basket
            basket_items = BasketItem.objects.filter(ProductID=ProductID, BasketID=shopping_basket).first()
            if basket_items:
                if basket_items.Quantity > 1:
                    basket_items.Quantity = basket_items.Quantity - 1 # if it is already in the basket, add to the quantity
                    basket_items.save()
                    return basket_items
                else:
                    basket_items.delete()
                    return BasketItem(BasketID=shopping_basket, ProductID=ProductID, Quantity=0)
            else:
                return BasketItem(BasketID=shopping_basket, ProductID=ProductID, Quantity=0)
        else:
            return None

class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['BasketID', 'ShippingCountry', 'ShippingAddress1', 'ShippingAddress2', 'ShippingAddressZip']

    def create(self, validated_data):
        request = self.context.get('request', None)
        current_user = request.user
        BasketID = validated_data['BasketID']
        ShpC = validated_data['ShippingCountry']
        Shp1 = validated_data['ShippingAddress1']
        Shp2 = validated_data['ShippingAddress2']
        ShpZip = validated_data['ShippingAddressZip']
        # get the sopping basket
        # mark as inactive
        BasketID.is_active = False
        BasketID.save()
        # Get the individual items and show the total
        SBI = BasketItem.objects.filter(BasketID = BasketID)
        total = 0.0
        for item in SBI:
            total += float(item.Price())
        # create a new order 
        order = Order.objects.create(BasketID = BasketID, UserID = current_user, ShippingCountry = ShpC, ShippingAddress1 = Shp1, ShippingAddress2 = Shp2, ShippingAddressZip = ShpZip, TotalPrice = total )
        # create a new empty basket for the customer 
        # new_basket = Basket.objects.create(user_id = current_user)# Create a shopping basket 
        # return the order
        return order

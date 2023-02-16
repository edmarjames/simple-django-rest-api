# import dependencies
from rest_framework import serializers

# import model
from . models import Product

# create a serializer class
class ProductSerializer(serializers.ModelSerializer):

    # create a class Meta "M" should be capital
    class Meta:
        # declare the model
        model = Product
        # declare the fields, always include the 'id'
        fields = ['id', 'name', 'description', 'price', 'active']

# import dependencies
from rest_framework             import serializers

# import model/s
from . models                   import Product
# import default User model
from django.contrib.auth.models import User


# create a serializer class
class ProductSerializer(serializers.ModelSerializer):

    # create a class Meta "M" should be capital
    class Meta:
        # declare the model
        model = Product
        # declare the fields, always include the 'id'
        fields = ['id', 'name', 'description', 'price', 'active']

class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

        # keyword arguments
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        # validation
        user = User(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
        )

        # validation
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        # checks if password and password2 match
        if password != password2:
            raise serializers.ValidationError({'password': 'Sorry, the password did not match'})
        
        # hash the password
        user.set_password(password)

        # save the user
        user.save()

        return user
    
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# Yes, there are other options available in addition to serializer.data to access the serialized data in Django serializers.

# serializer.validated_data: This attribute returns a dictionary of deserialized data after validating the incoming data. This is useful when you want to work with the deserialized data in your view or API endpoint.

# serializer.instance: This attribute returns the instance that the serializer was initialized with. This is useful when you want to update an existing object with the data that was sent in the request.

# serializer.data.items(): You can use the items() method to get the serialized data as key-value pairs. This is useful when you need to iterate over the serialized data in a loop.

# serializer.data.values(): You can use the values() method to get a list of the serialized data values. This is useful when you need to perform an operation on all the values in the serialized data.

# serializer.data.get('field_name'): You can use the get() method to get a specific value from the serialized data by providing the name of the field. This is useful when you need to retrieve a specific value from the serialized data.
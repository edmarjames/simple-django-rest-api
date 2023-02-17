# import dependencies
from rest_framework import serializers

# import model
from . models import Product
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
from django.shortcuts                   import render

# import Response, api_view, status and Token from rest framework
from rest_framework.response            import Response
from rest_framework.decorators          import api_view
from rest_framework                     import status
from rest_framework.authtoken.models    import Token

# import product model
from . models                           import Product
# import User model
from django.contrib.auth.models         import User

# import serializer
from . serializers                      import ProductSerializer, RegistrationSerializer, UserSerializer



# declare the HTTP method
@api_view(['GET', 'POST'])
# format=None is added to obtain the results in json format in the browser
def product_list(request, format=None):
    
    if request.method == 'GET':
        # get all of the products/get a list of all the products
        products = Product.objects.all()

        print(products)

        # pass it to 'ProductSerializer', 'many=True' means to serialize everything
        serializer = ProductSerializer(products, many=True)

        # use 'Response' when providing the API response
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # get the data from the request body and deserialize it
        serializer = ProductSerializer(data=request.data)

        # check if it is valid
        if serializer.is_valid():
            # save it
            serializer.save()

            message = {
                "message": "Product added successfully!",
                "data": serializer.data,
                "status": status.HTTP_201_CREATED
            }

            # returns the data of the added product
            return Response(message)
        
        # provide an error message if the request body is incomplete
        else:
            message = {
                "message": "Something went wrong!",
                "status": status.HTTP_204_NO_CONTENT
            }

            return Response(message)

@api_view(['GET', 'PUT', 'DELETE'])
def single_product(request, pk, format=None):
    
    # checks if the product_id exists on the database
    try:
        product = Product.objects.get(id=pk)

    # throw an error if product_id does not exist
    except Product.DoesNotExist():
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # checks if the HTTP method is 'GET'
    if request.method == 'GET':
        # pass it to the serializer
        serializer = ProductSerializer(product)

        # return the data of the product
        return Response(serializer.data)

    elif request.method == 'PUT':
        # on this case the 'ProductSerializer' receives two arguments, first one is 'product' which is the fetched data from the database and 'data=request.data' which is the input from the request body
        serializer = ProductSerializer(product, data=request.data)

        # check if it is valid
        if serializer.is_valid():
            # save it
            serializer.save()

            message = {
                "message": "Product updated successfully!",
                "data": serializer.data
            }

            # returns the data of the added product
            return Response(message)

        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        
    elif request.method == 'DELETE':
        # use .delete() method to delete the product
        product.delete()

        message = {
            "message": "Product deleted successfully!",
            "status": status.HTTP_204_NO_CONTENT
        }

        return Response(message)

@api_view(['PATCH'])
def archive_or_activate_product(request, pk, format=None):

    # check if the product exists
    try:
        product = Product.objects.get(id=pk)
    
    # throw an error if product does not exist
    except Product.DoesNotExist():
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # check if the HTTP method is PATCH
    if request.method == 'PATCH':

        # if the product is active, we archive it and modify the message string
        if product.active == True:
            product.active = False
            message = "Product archived successfully!"

        # else if the product is inactive, we activate it and modify the message string
        elif product.active == False:
            product.active = True
            message = "Product activated successfully!"

        product.save()
        serializer = ProductSerializer(product)

        result = {
            "message": message,
            "details": serializer.data,
            "status": status.HTTP_200_OK
        }

        return Response(result)
    
@api_view(['GET'])
def get_all_products(request, format=None):

    # checks if the HTTP method is GET
    if request.method == 'GET':

        # filter the active products from Product model
        products = Product.objects.filter(active=True)

        # serialize it
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)
    
@api_view(['POST'])
def register(request):

    # checks if the HTTP method is POST
    if request.method == 'POST':

        # get the data from the request body
        serializer = RegistrationSerializer(data=request.data)
        

        # declare an empty dict
        data = {}

        if serializer.is_valid():

            # usage of serializer.validated_data
            validated = serializer.validated_data
            print(validated)
            print(validated['username'])

            # create a new user
            user = serializer.save()

            # add a 'response' property to the data dict
            data['response'] = 'Successfully registered a new user!'

            # get the token of the current logged in user, 'key' means get the raw authentication token
            auth_token = Token.objects.get(user=user).key
            
            # add a 'auth_token' property to the data dict
            data['token'] = auth_token

        else:
            data = serializer.errors

        return Response(data)
    
@api_view(['GET'])
def get_users(request, pk = None):

    # checks if the request method is 'GET'
    if request.method == 'GET':

        result = {}

        if pk:
            specific_user = User.objects.get(id=pk)

            if specific_user is not None:
                serializer = UserSerializer(specific_user)
            else:
                result['error'] = status.HTTP_404_NOT_FOUND

            # usage of serializer.data.items()
            for key, value in serializer.data.items():
                print(f'{key} => {value}')

            # usage of serializer.data.values()
            values = serializer.data.values()
            print(values)

            # usage of serializer.data.get('field')
            username = serializer.data.get('username')
            print(f'This is the username {username}')

        else:
            # get all the users from User model
            users = User.objects.all()

            # serialize it
            serializer = UserSerializer(users, many=True)

        result['data'] = serializer.data

        return Response(result)
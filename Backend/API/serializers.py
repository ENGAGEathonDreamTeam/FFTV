# Import necessary modules
from rest_framework import serializers
from .models import CustomUser

# Define UserSerializer which inherits from ModelSerializer.
# This will allow the serializer to automatically generate fields based on the CustomUser model.
class UserSerializer(serializers.ModelSerializer):
    # Meta class is used by Django to store some extra information about the ModelSerializer.
    class Meta:
        # The model that this serializer should use is the CustomUser model, which we define in prototype/models
        model = CustomUser
        # The fields of the model to be included in the serialized representation.
        fields = ['username', 'email', 'password', 'user_bio']
        # extra_kwargs is used to add any additional arguments into a field.
        # Here, we are setting the 'password' field to write_only, which means it won't be included when rendering to JSON.
        extra_kwargs = {'password': {'write_only': True}}

    # Define the create method. This is called when we create a new user instance.
    def create(self, validated_data):
        # Pop the password from validated_data dictionary as it will be handled separately.
        password = validated_data.pop('password')
        # Create a CustomUser instance using the remaining validated data.
        user = CustomUser(**validated_data)
        # Set the user's password using Django's built-in set_password method. This will handle hashing and salting of the password.
        user.set_password(password)
        # Save the user instance to the database.
        user.save()
        # Return the user instance.
        return user

    # Define the update method. 
    def update(self, instance, validated_data):
        # handle password separately
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

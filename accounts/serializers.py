from rest_framework import serializers
from django.contrib.auth.models import User

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password should not be returned in responses
    referral_code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'referral_code']

    def create(self, validated_data):
        # This method is called when serializer.save() is called
        # Create user with hashed password (using create_user helper)
        referral_code = validated_data.pop('referral_code', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        # Optionally handle referral_code logic here
        return user

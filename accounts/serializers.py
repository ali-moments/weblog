from rest_framework import serializers
from .models import Users  # Use your custom Users model

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password should not be returned in responses
    referral_code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Users
        fields = ['email', 'password', 'referral_code']

    def create(self, validated_data):
        # Extract referral code if provided
        referral_code = validated_data.pop('referral_code', None)

        # Create the user
        user = Users.objects.create(
            email=validated_data['email'],
            password=validated_data['password']
        )

        # If a referral code is provided, link the user to the referrer
        if referral_code:
            try:
                referrer = Users.objects.get(referral_code=referral_code)
                user.referred_by = referrer
                user.save()
            except Users.DoesNotExist:
                pass  # Ignore if the referral code is invalid

        return user

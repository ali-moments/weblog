from rest_framework import serializers
from .models import Users  # Use your custom Users model

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password should not be returned in responses
    referral_code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Users
        fields = ['email', 'password', 'referral_code']

    def validate_referral_code(self, value):
        if value and not Users.objects.filter(referral_code=value).exists():
            raise serializers.ValidationError("Invalid referral code.")
        return value

    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', None)

        user = Users.objects.create(
            email=validated_data['email'],
            password=validated_data['password']
        )

        if referral_code:
            referrer = Users.objects.filter(referral_code=referral_code).first()
            if referrer:
                user.referred_by = referrer
                user.save()

        return user

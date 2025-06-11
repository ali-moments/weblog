from rest_framework import serializers
from .models import Users  # Use your custom Users model

class UserSignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)
    referral_code = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Users
        fields = ['email', 'username', 'password', 'referral_code']

    def validate_username(self, value):
        if Users.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def validate_referral_code(self, value):
        if value and not Users.objects.filter(referral_code=value).exists():
            raise serializers.ValidationError("Invalid referral code.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        referral_code = validated_data.pop('referral_code', None)

        user = Users.objects.create(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()

        if referral_code:
            referrer = Users.objects.filter(referral_code=referral_code).first()
            if referrer:
                user.referred_by = referrer
                user.save()

        return user

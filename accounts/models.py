from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=300)
    referral_code = models.CharField(max_length=100, blank=True, null=True)  # Field for referral code
    referred_by = models.ForeignKey(
        'self', on_delete=models.SET_NULL, blank=True, null=True, related_name='referrals'
    )  # Tracks who referred the user
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

from django.contrib.auth.models import User
from rest_framework import serializers
from base.models import Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= ['id', 'username', 'email', 'first_name', 'last_name','is_superuser']

class ProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    profile_image=serializers.ImageField(required=False)

    class Meta:
        model=Profile
        fields=['user','profile_image']

class RegistrationSerializer(serializers.ModelSerializer):
    profile= ProfileSerializer(required=False)

    class Meta:
        model = User
        fields=('username','password','email','profile','first_name','last_name')
        
    def create(self, validated_data):
        profile_data= validated_data.pop('profile',None)
        user = User.objects.create_user(**validated_data)

        if profile_data:
            Profile.objects.create(user=user,**profile_data)

        return user
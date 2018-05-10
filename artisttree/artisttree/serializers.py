from rest_framework import serializers
from .models import User, UserProfileInfo


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = '__all__'


class UserProfileInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = '__all__'
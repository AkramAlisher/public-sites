from rest_framework import serializers

from django.contrib.auth.models import User

from api.models import Cargo, Vehicle, Profile


class CargoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta():
        model = Cargo
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta():
        model = Vehicle
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta():
        model = User
        fields = ('id', 'username', 'email', 'password')


class ProfileSerializer(serializers.ModelSerializer):

    class Meta():
        model = Profile
        fields = ('phone', 'user')


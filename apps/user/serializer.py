from rest_framework import  serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.user.models import User

# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# Login serializer
class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(LoginSerializer, self).validate(attrs)
        data.update({'id': self.user.id})
        data.update({'first_name': self.user.first_name})
        data.update({'last_name': self.user.last_name})
        data.update({'email': self.user.email})
        return data

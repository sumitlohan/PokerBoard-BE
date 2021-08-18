from rest_framework import  serializers
from rest_framework.authtoken.models import Token

from apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password','token']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_token(self, user):
        return Token.objects.get_or_create(user = user)[0].key

    def create(self, validated_data):
        user = User(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

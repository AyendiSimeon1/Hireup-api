from rest_framework import serializers
from django.contrib.auth import get_user_model
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email


User = get_user_model()

class ProfileSerializer(serializers.Serializer):
    model = User
    fields = ['id', 'email', 'username']

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)


    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username
    
    def validate_password1(self, password):
        return get_adapter().clean_username(password)

    def validate(self, data):

        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields do not match")

        return data
    def save(self, request):
        user = User(username=self.validated_data['username'], email=self.validated_data['email'])
        user.set_password(self.validated_data['password1'])
        user.save()
        setup_user_email(request, user, [])
        return user
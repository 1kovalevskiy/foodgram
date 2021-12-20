from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'id',
            'first_name',
            'last_name',
            'is_subscribed',
            'password'
        )
        write_only_fields = ('password',)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        del rep["password"]
        return rep

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = super().create(validated_data=validated_data)
        instance.set_password(password)
        instance.save()
        return instance

    def get_is_subscribed(self, obj):
        request = self.root.context.get('request')
        try:
            user = request.user
        except AttributeError:
            return False
        if isinstance(user, AnonymousUser):
            return False
        elif user == obj:
            return False
        return User.objects.filter(id=user.pk).filter(
            follower__author_id=obj.pk).exists()


class PasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from recipes.models import Recipe
from users.models import Follow

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

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


class RecipesMiniSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='author.email', read_only=True)
    id = serializers.PrimaryKeyRelatedField(source='author.id', read_only=True)
    username = serializers.CharField(source='author.username', read_only=True)
    first_name = serializers.CharField(
        source='author.first_name', read_only=True
    )
    last_name = serializers.CharField(
        source='author.last_name', read_only=True
    )
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipesMiniSerializer(source='author.recipes',
                                    read_only=True,
                                    many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes_count', 'recipes'
        )

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.root.context.get('request')
        if request is not None:
            count = request.query_params.get('recipes_limit')
        else:
            count = self.root.context.get('recipes_limit')
        if count is not None:
            rep['recipes'] = rep['recipes'][:int(count)]
        return rep

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()

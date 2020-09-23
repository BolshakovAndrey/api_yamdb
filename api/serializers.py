from rest_framework import serializers
from .models import User, Roles, Comment, Review


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(default=Roles.USER)

    class Meta:
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role', 'confirmation_code')
        model = User
        extra_kwargs = {'confirmation_code': {'write_only': True},
                        'username': {'required': True},
                        'email': {'required': True}}


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment

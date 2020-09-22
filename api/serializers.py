from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    # group = serializers.SlugRelatedField(read_only=True, slug_field='name')
    role = serializers.CharField(source='get_role_display')

    class Meta:
        fields = ('first_name', 'last_name', 'username',
                  'bio', 'email', 'role', 'confirmation_code')
        model = User
        extra_kwargs = {'confirmation_code': {'write_only': True}}

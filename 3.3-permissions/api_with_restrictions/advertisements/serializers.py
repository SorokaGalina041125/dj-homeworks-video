from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""
    creator = UserSerializer(read_only=True)
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', 'is_favorite')

    def get_is_favorite(self, obj):
        """Проверяет, добавил ли пользователь объявление в избранное"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj in request.user.favorite_ads.all()
        return False

    def create(self, validated_data):
        """Метод для создания."""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        request = self.context.get('request')
        
        # Проверка на количество открытых объявлений (не больше 10)
        if request and request.method == 'POST':
            status = data.get('status', Advertisement.OPEN)
            if status == Advertisement.OPEN:
                open_ads_count = Advertisement.objects.filter(
                    creator=request.user,
                    status=Advertisement.OPEN
                ).count()
                if open_ads_count >= 10:
                    raise ValidationError(
                        'У вас уже 10 открытых объявлений. '
                        'Закройте одно, чтобы создать новое.'
                    )
        return data


class AdvertisementCreateSerializer(serializers.ModelSerializer):
    """Serializer для создания объявления."""
    class Meta:
        model = Advertisement
        fields = ('title', 'description', 'status')
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer, AdvertisementCreateSerializer
from advertisements.filters import AdvertisementFilter
from advertisements.permissions import IsOwnerOrAdminOrReadOnly


class AdvertisementViewSet(viewsets.ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AdvertisementFilter
    ordering_fields = ['price', 'created_at']
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly]

    def get_permissions(self):
        """Получение прав для действий."""
        # Для создания, обновления и удаления нужна авторизация
        if self.action in ["create", "update", "partial_update", "destroy", 
                           "favorite", "unfavorite"]:
            return [IsAuthenticated()]
        return [IsAuthenticatedOrReadOnly()]

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия."""
        if self.action == 'create':
            return AdvertisementCreateSerializer
        return AdvertisementSerializer

    def perform_create(self, serializer):
        """При создании автоматически проставляем creator."""
        serializer.save(creator=self.request.user)

    # Дополнительное задание: избранное
    @action(detail=True, methods=['POST'], url_path='favorite')
    def favorite(self, request, pk=None):
        """Добавить объявление в избранное."""
        advertisement = self.get_object()
        
        # Нельзя добавить в избранное свое объявление
        if advertisement.creator == request.user:
            return Response(
                {'detail': 'Нельзя добавить в избранное свое объявление'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.favorite_ads.add(advertisement)
        return Response({'detail': 'Добавлено в избранное'})

    @action(detail=True, methods=['POST'], url_path='unfavorite')
    def unfavorite(self, request, pk=None):
        """Удалить объявление из избранного."""
        advertisement = self.get_object()
        request.user.favorite_ads.remove(advertisement)
        return Response({'detail': 'Удалено из избранного'})

    @action(detail=False, methods=['GET'], url_path='my-favorites')
    def my_favorites(self, request):
        """Получить все избранные объявления пользователя."""
        favorites = request.user.favorite_ads.all()
        serializer = self.get_serializer(favorites, many=True)
        return Response(serializer.data)
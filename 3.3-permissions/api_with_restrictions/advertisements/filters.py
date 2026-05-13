from django_filters import rest_framework as filters
from advertisements.models import Advertisement, AdvertisementStatusChoices


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    created_at = filters.DateFromToRangeFilter(field_name='created_at')
    status = filters.ChoiceFilter(choices=AdvertisementStatusChoices.choices)
    favorite = filters.BooleanFilter(method='filter_favorite')

    def filter_favorite(self, queryset, name, value):
        """Фильтрация по избранным объявлениям."""
        request = self.request
        if value and request and request.user.is_authenticated:
            return queryset.filter(favorites=request.user)
        return queryset

    class Meta:
        model = Advertisement
        fields = ['status', 'created_at', 'favorite']
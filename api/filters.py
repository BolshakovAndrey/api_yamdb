import django_filters

from api.models import Title


class TitleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='contains')
    category = django_filters.CharFilter(field_name='category__slug', )
    genre = django_filters.CharFilter(field_name='genre__slug', )

    class Meta:
        model = Title
        fields = {'name', 'year', 'genre', 'category'}

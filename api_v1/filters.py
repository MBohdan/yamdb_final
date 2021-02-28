from django_filters import rest_framework as filters

from .models import Title


class TitleFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    category = filters.CharFilter(
        field_name="category__slug", lookup_expr="iexact"
    )
    genre = filters.CharFilter(field_name="genre__slug", lookup_expr="iexact")

    class Meta:
        model = Title
        fields = ("name", "year", "category", "genre")

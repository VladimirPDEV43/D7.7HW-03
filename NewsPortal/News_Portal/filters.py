import django_filters
from django import forms
from django_filters import FilterSet
from .models import Post, Author


class PostFilter(FilterSet):
    name = django_filters.CharFilter(field_name='header_post',
                                     label="Поиск по названию",
                                     lookup_expr='icontains', )
    author = django_filters.ModelChoiceFilter(field_name='authors',
                                              label='Выбор автора',
                                              lookup_expr='exact',
                                              queryset=Author.objects.all())
    date = django_filters.DateFilter(field_name='time_of_publication',
                                     widget=forms.DateInput(attrs={'type': 'date'}),
                                     label='Дата',
                                     lookup_expr='date__gte')
    text = django_filters.CharFilter(field_name='text_post',
                                     label="Поиск по тексту",
                                     lookup_expr='contains', )

    class Meta:
        model = Post
        fields = []

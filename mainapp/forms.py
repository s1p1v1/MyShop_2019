from django import forms

from mainapp.models import Country

RATING_CHOICES = (
    (0, 'нет оценки'),
    (1, 'неудовлетворительно'),
    (2, 'удовлетворительно'),
    (3, 'хорошо'),
    (4, 'отлично'),
)

SORTING_CHOICES = (
    (0, 'по убыванию'),
    (1, 'по возрастанию'),
)

ATTRIBUTE_CHOICES = (
    (1, 'по цене'),
    (2, 'по рейтингу'),
)

COUNTRY_CHOICES = [(0, 'Все страны')]
country_list = [(i.id, i.name) for i in Country.objects.filter(is_active=True)]
COUNTRY_CHOICES.extend(country_list)
tuple(COUNTRY_CHOICES)
print(COUNTRY_CHOICES)


class ProdRatingForm(forms.Form):
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect(),
                               initial=0, label='Выберите из списка:')


class SearchForm(forms.Form):
    search = forms.CharField(initial='', label='', required=False)


class ProdSortForm(forms.Form):
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, label='Страны')
    # country = forms.ModelChoiceField(queryset=Country.objects.filter(is_active=True), label='Страны', empty_label='Все страны')
    price_rating = forms.ChoiceField(choices=ATTRIBUTE_CHOICES, initial=0, label='Цена/Рейтинг')
    sorting_direction = forms.ChoiceField(choices=SORTING_CHOICES, initial=0, label='По убыванию/возрастанию')

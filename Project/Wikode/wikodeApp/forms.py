from django import forms
from wikodeApp.models import RegistrationApplication
from dal import autocomplete
from functools import partial


DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class FilterForm(forms.Form):
    start_date = forms.DateField(widget=DateInput(), required=False)
    end_date = forms.DateField(widget=DateInput(), required=False)
    author_field = forms.CharField(label='Author', max_length=100, required=False)
    journal_field = forms.CharField(label='Journal', max_length=100, required=False)
    keywords_field = forms.CharField(label='Keywords', max_length=100, required=False)


class ApplicationRegistrationForm(forms.ModelForm):

    class Meta:
        model = RegistrationApplication
        fields = ('name', 'surname', 'email', 'applicationText')


class GetArticleForm(forms.Form):
    article_topic = forms.CharField(label='Topic', max_length=100)
    volume = forms.CharField(label='# of Articles', max_length=100)


class TagForm(forms.Form):
    wikiLabel = autocomplete.Select2ListChoiceField(
        widget=autocomplete.ListSelect2(url='tag-autocomplete'),
        label="Search Wikidata Entry"
    )

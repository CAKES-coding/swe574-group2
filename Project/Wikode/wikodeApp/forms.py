from django import forms
from wikodeApp.models import RegistrationApplication
from dal import autocomplete


class ApplicationRegistrationForm(forms.ModelForm):

    class Meta:
        model = RegistrationApplication
        fields = ('name', 'surname', 'email', 'applicationText')


class GetArticleForm(forms.Form):
    article_topic = forms.CharField(label='Topic', max_length=100)
    volume = forms.CharField(label='# of Articles', max_length=100)

class TagForm(forms.Form):
    wikiLabel = autocomplete.Select2ListChoiceField(
        widget=autocomplete.ListSelect2(url='wikode/tag-autocomplete'),
        label="Search Wikidata Entry"
    )

from django import forms
from wikodeApp.models import RegistrationApplication
from dal import autocomplete


class ApplicationRegistrationForm(forms.ModelForm):

    class Meta:
        model = RegistrationApplication
        fields = ('name', 'surname', 'email', 'applicationText')


class TagForm(forms.Form):
    wikiLabel = autocomplete.Select2ListChoiceField(
        widget=autocomplete.ListSelect2(url='tag-autocomplete'),
        label="Search Wikidata Entry"
    )

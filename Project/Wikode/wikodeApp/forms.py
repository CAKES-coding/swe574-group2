from django import forms
from wikodeApp.models import RegistrationApplication


class ApplicationRegistrationForm(forms.ModelForm):

    class Meta:
        model = RegistrationApplication
        fields = ('name', 'surname', 'email', 'applicationText')
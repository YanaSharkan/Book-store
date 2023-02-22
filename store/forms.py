from datetime import timedelta

from django import forms
from django.utils import timezone

from store.models import Author


class ReminderForm(forms.Form):
    email = forms.EmailField(initial='test@test.com')
    text = forms.CharField(initial='test reminder text')
    date_time = forms.DateTimeField(initial=timezone.now())

    def clean_date_time(self):
        value = self.cleaned_data["date_time"]
        max_value = timezone.now() + timedelta(days=2)
        if value < timezone.now() or value > max_value:
            raise forms.ValidationError("date_time not valid")
        return value


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'age']

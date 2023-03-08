from django import forms
from django.utils.translation import gettext_lazy as _
from taggit.forms import TagField


class ManageTagsForm(forms.Form):
    tags = TagField(
        label=_('Tags'),
        help_text=_('Comma or space seperated list of tags.'),
        max_length=255)


class IncludeForm(forms.Form):
    ERROR_MSG = 'At least one include option must be checked.'

    def clean(self):
        """
        At least one include option must be checked.
        """
        cleaned_data = super().clean()

        if not any(cleaned_data.values()):
            raise forms.ValidationError(self.ERROR_MSG)

        return cleaned_data

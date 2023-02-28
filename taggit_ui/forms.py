from django import forms
from django.utils.translation import gettext_lazy as _
from taggit.forms import TagField


class ManageTagsForm(forms.Form):
    tags = TagField(
        label=_('Tags'),
        help_text=_('Comma or space seperated list of tags.'),
        max_length=255)


class IncludeForm(forms.Form):
    def clean(self):
        """
        At least one include option must be checked.
        """
        cleaned_data = super().clean()

        if not any(cleaned_data.values()):
            msg = 'At least one include option must be checked.'
            raise forms.ValidationError(msg)

        return cleaned_data

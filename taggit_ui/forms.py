from django import forms
from taggit.forms import TagField


class ManageTagsForm(forms.Form):
    tags = TagField(
        label='Tags',
        help_text='Comma or space seperated list of tags.',
        max_length=255,
        )

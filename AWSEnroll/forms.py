from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from . import validators 

class UserAddForm(forms.Form):

    projectName = forms.CharField(max_length=100)

    email = forms.EmailField(
        help_text=_(u'email address'),
        required=False,
        validators=[
            validators.validate_confusables_email,
        ]
    )

class UserDeleteForm(forms.Form):

    name = forms.CharField(max_length=100)

class InviteForm(forms.Form):

    emailOne = forms.EmailField(
        help_text=_(u'email address'),
        required=True,
        validators=[
            validators.validate_confusables_email,
        ]
    )
    emailTwo = forms.EmailField(
        help_text=_(u'email address'),
        required=False,
        validators=[
            validators.validate_confusables_email,
        ]
    )
    emailThree = forms.EmailField(
        help_text=_(u'email address'),
        required=False,
        validators=[
            validators.validate_confusables_email,
        ]
    )

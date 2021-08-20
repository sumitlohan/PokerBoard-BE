import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class CustomPasswordValidator():

    def validate(password):
        if len(password) < 8:
            raise ValidationError(_('This password is too short. It must contain at least 8 characters.'))
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('Password must contain at least 1 digit.'))
        if not any(char.isalpha() for char in password):
            raise ValidationError(_('Password must contain at least 1 letter.'))
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(_('Password must contain at least 1 special character.'))
        if not re.findall('[A-Z]', password):
            raise ValidationError(_("The password must contain at least 1 uppercase letter, A-Z."))

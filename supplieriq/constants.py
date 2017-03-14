"""
Purpose: Constants for User Management.
This file includes all the constant values used in user management.

Constraints:
"""
from django.utils.translation import ugettext as _
from django.conf import settings
import datetime

FIRST_NAME_MAX_LENGTH = 30
LAST_NAME_MAX_LENGTH = 30
USER_NAME_MAX_LENGTH = 27

# userena settings
PASSWORD_MIN_LENGTH = getattr(settings, 'USERENA_RF_PASSWORD_MIN_LENGTH', 6)

# attrs for various form fields widgets
ATTRS_DICT = {'required': 'true'}
ATTRS_DICT_FIRST_NAME = {"placeholder": _(u'First name'), "autofocus": "autofocus"}
ATTRS_DICT_LAST_NAME = {"placeholder": _(u'Last name')}
ATTRS_DICT_EMAIL = {"placeholder": _(u'Your email address'),
                    'autocomplete': 'off'
                    }
ATTRS_DICT_EMAIL2 = {"placeholder": _(u'Re-enter email address'),
                     'autocomplete': 'off' }
ATTRS_DICT_CAPTCHA = {"placeholder": _(u'Enter the above code here')}
ATTRS_DICT_PASSWORD1 = {"placeholder": _(u'Enter password'), 'autocomplete': 'off', }
ATTRS_DICT_PASSWORD2 = { "placeholder": _(u'Confirm password'), 'autocomplete': 'off', }
ATTRS_DICT_DOB = {"placeholder": _(u'Enter Date of Birth')}
ATTRS_DICT_IDENTIFICATION = { "placeholder": _(u'Enter Email'), "autofocus": "autofocus"}
ATTRS_DICT_ZIPCODE = {"placeholder": _(u'Zipcode/Postal code')}
ATTRS_DICT_ZIPCODE = {"placeholder": _(u'Zipcode/Postal code')}
ENTER_ADDRESS = {"placeholder": _(u'Enter Address, City, State or Zip')}
ATTRS_DICT_POSTAL = {"placeholder": _(u'Zipcode/Postal code'), "maxlength":6}

"""
Purpose: Constants for User Management.
This file includes all the constant values used in user management.

Constraints:
"""
from django.utils.translation import ugettext as _
from django.conf import settings
import datetime
from wiki.other_settings.s3_settings import STATIC_URL
if settings.LOCAL_DEV:
    STATIC_URL = settings.STATIC_URL

MEMBERSHIP_LEVELS = (
    ('0', _('N.A.')),
    ('1', _('Expert User')),
    ('2', _('Administrator')),
    )

GENDERS = (
    ('m', _('Male')),
    ('f', _('Female')),
    )

COUNTRIES = (
    ("usa", _("United States")),
    ("can", _("Canada")),
    )


COUNTRIES_LIST = [{'text': u'United States', 'value': 'US'}, {'text': u'Canada', 'value': 'CN'}]
COUNTRY_CONSTANT = 'US'
VANITY_URL_MAX_LEN = 10
MOBILE_CODE_MAX_LEN = 6
MOBILE_NO_MAX_LEN = 10
ABOUT_US_MAX_LEN = 250

DOB_LIMIT = 13
MIN_YEAR = 1900
MAX_YEAR = datetime.datetime.now().year+1
PEOPLE_URL_FIELD = 'user__username'


ZIPCODE_MIN_LENGTH = 5
ZIPCODE_MAX_LENGTH = 6
USER_ZIPCODE_MAX_LENGTH = 5

ADDR_MAX_LENGTH = 30
CITY_MAX_LENGTH = 30
STATE_MAX_LENGTH = 30
FIRST_NAME_MAX_LENGTH = 30
LAST_NAME_MAX_LENGTH = 30
USER_NAME_MAX_LENGTH = 27

# userena settings
API_MESSAGE_KEY = getattr(settings, 'USERENA_RF_API_MESSAGE_KEY', 'message')
USERNAME_RE = getattr(settings, 'USERENA_RF_USERNAME_RE', r'^[\.\w]+$')
PASSWORD_MIN_LENGTH = getattr(settings, 'USERENA_RF_PASSWORD_MIN_LENGTH', 6)
USER_SERIALIZER_CLASS = getattr(
    settings,
    'USERENA_RF_USER_SERIALIZER_CLASS',
    'userena_rf.serializers.ProfileSerializer',
    )

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
MONTHS = {
    '01': _('January'), '02': _('February'),
    '03': _('March'), '04': _('April'),
    '05': _('May'), '06': _('June'),
    '07': _('July'), '08': _('August'), '09': _('September'),
    '10': _('October'), '11': _('November'),
    '12': _('December')
}

SEARCH_PROFILE = """{"query":{"match": {"id": %s}}}"""

FEEDS_PAGINATE_BY = 10

PROJECT_TOKEN = '00d011ab1b6b7204b147b819630bf57f'

CHOICES_SELECT = [('working', 'Working'),
         ('exists', 'Exists')]

BIZ_DOMAIN = "biz.wikireviews.com"

OWNER_DEFAULT_PATH = STATIC_URL + "images/circle.png"

#
# DEFAULT_PRIVACY_DICT = {'private_msgs': 'jst_my_frnd',
#  'reviews': {"allow_non_friends": "Allow non-friends to Follow my reviews"},
#  'view_my_profile': 'all_wiki'}

# changed for new setttings
DEFAULT_PRIVACY_DICT = {"view_my_profile":"everyone",
"who_can_send_friend_request":"everyone",
"link_search_engine_timelines":"yes",
"temperature_setting":"f",
"measurement_setting":"us_measurement_system"}


FIELDS_DISABLED_LIST = ['email_me_new_edition', 'add_as_friend', 'unsubscribe_all_email', 'friend_recieves_badge_icon', 'confirms_friend', \
                       'select_actions_on_content', 'selects_for_wiki_badge_icon', 'follow_my_review', 'comments_on_my_review', \
                       'send_me_request', 'add_as_frnd', 'select_for_badge', 'confirm_friend_request', \
                       'snd_msg', 'comments_on_review', 'follow_reviews', 'friends_recieves_badge', 'anonymous_reviews_all', \
                       'allow_non_friends']


TRENDING_CITY_QUERY ="""select DISTINCT entry.id FROM reviews_userentries entry inner join users_address address on entry.id = address.entries_id   inner join reviews_userentries_primary_media media on entry.id = media.user_entries_id INNER JOIN review_review rr ON rr.associated_to_id    = entry.id INNER JOIN reviews_userentries_taxonomy rut ON rut.userentries_id = entry.id WHERE (address.city = '%s' or address.`state` = '%s') ORDER BY rr.created_date_time desc;"""

HOME_BUSINESS_CATEGORY_TRENDING_QUERY = """
SELECT DISTINCT rue.id 
    FROM reviews_userentries rue 
    INNER JOIN users_address ua 
    ON rue.id                     = ua.entries_id   
    INNER JOIN reviews_userentries_primary_media media 
    ON rue.id                     = media.user_entries_id 
    LEFT OUTER JOIN review_review rr 
    ON rr.associated_to_id        = rue.id
    INNER JOIN reviews_userentries_taxonomy ruet
    ON ruet.taxonomy_id            = %s AND
       ruet.userentries_id        = rue.id
    WHERE (3956 * 2 * ASIN(SQRT(POWER(SIN((%s - ABS(ua.latitude)) * PI()/180 / 2), 2) +  COS(%s * PI()/180 ) * COS(ABS(ua.latitude) * PI()/180) * POWER(SIN((%s - ua.longitude) * PI()/180 / 2), 2) ))) < 200
    ORDER BY (3956 * 2 * ASIN(SQRT(POWER(SIN((%s - ABS(ua.latitude)) * PI()/180 / 2), 2) +  COS(%s * PI()/180 ) * COS(ABS(ua.latitude) * PI()/180) * POWER(SIN((%s - ua.longitude) * PI()/180 / 2), 2) )))
    LIMIT 6;
"""

# TRENDING_CITY_QUERY_PRIMARY ="""select DISTINCT entry.id FROM reviews_userentries entry inner join users_address address on entry.id = address.entries_id   inner join reviews_userentries_primary_media media on entry.id = media.user_entries_id INNER JOIN review_review rr ON rr.associated_to_id    = entry.id WHERE (3956 * 2 * ASIN(SQRT(POWER(SIN((%s - abs(address.latitude)) * pi()/180 / 2), 2) +  COS(%s * pi()/180 ) * COS(abs(address.latitude) * pi()/180) * POWER(SIN((%s - address.longitude) * pi()/180 / 2), 2) ))) < 20 ORDER BY rr.created_date_time desc;"""
TRENDING_CITY_QUERY_PRIMARY ="""select DISTINCT a.id FROM (select entry.id FROM reviews_userentries entry inner join users_address address on entry.id = address.entries_id   inner join reviews_userentries_primary_media media on entry.id = media.user_entries_id INNER JOIN review_review rr ON rr.associated_to_id    = entry.id WHERE (3956 * 2 * ASIN(SQRT(POWER(SIN((%s - abs(address.latitude)) * pi()/180 / 2), 2) +  COS(%s * pi()/180 ) * COS(abs(address.latitude) * pi()/180) * POWER(SIN((%s - address.longitude) * pi()/180 / 2), 2) ))) < 20 ORDER BY rr.created_date_time desc) a;"""

TRENDING_CITY_QUERY_SECONDARY = """  select DISTINCT entry.id
                        FROM reviews_userentries entry 
                        inner join users_address address 
                        on entry.id = address.entries_id   
                        inner join reviews_userentries_primary_media media 
                        on entry.id = media.user_entries_id 
                        INNER JOIN review_review rr
                        ON rr.associated_to_id    = entry.id
                        ORDER BY (3956 * 2 * ASIN(SQRT(POWER(SIN((%s - abs(address.latitude)) * pi()/180 / 2), 2) +  COS(%s * pi()/180 ) * COS(abs(address.latitude) * pi()/180) *  POWER(SIN((%s - address.longitude) * pi()/180 / 2), 2) ))); """

SUB_CAT_TRENDING_PRODUCT = """ select DISTINCT entry.id FROM reviews_userentries entry 
                        INNER JOIN reviews_userentries_taxonomy ruet
                        ON ruet.userentries_id  = entry.id AND
                           ruet.taxonomy_id   = %s
                        inner join reviews_userentries_primary_media media 
                        on entry.id = media.user_entries_id 
                        INNER JOIN reviews_userentries_statistics rues
                        ON rues.reviews_userentries_id = entry.id
                        ORDER BY rues.reviews_count DESC LIMIT 20;"""
                        
SUB_CAT_TRENDING_BUSINESS = """select DISTINCT entry.id,3956 * 2 * ASIN(SQRT(POWER(SIN((%s - abs(address.latitude)) * pi()/180 / 2), 2) +  COS(%s * pi()/180 ) * COS(abs(address.latitude) * pi()/180) *  POWER(SIN((%s - address.longitude) * pi()/180 / 2), 2) )) as  distance
                        FROM reviews_userentries entry 
                        INNER JOIN reviews_userentries_taxonomy ruet
                        ON ruet.userentries_id  = entry.id AND
                           ruet.taxonomy_id  = %s
                        inner join users_address address 
                        on entry.id = address.entries_id   
                        inner join reviews_userentries_primary_media media 
                        on entry.id = media.user_entries_id 
                        INNER JOIN reviews_userentries_statistics rues
                        ON rues.reviews_userentries_id    = entry.id
                        ORDER BY distance,rues.reviews_count DESC LIMIT 20;"""

FAVORITE_LIMIT = 20

RADIAL_DISTANCE_HISTORY = 0.0186411 #=30meters
# RADIAL_DISTANCE_HISTORY = 10


UNIQUEPIN = """SELECT UUID() AS `unique_id`,MIN(pin_id) AS id,user_entry_id,NULL AS review_id,profile_id,`type` FROM vw_user_pin_details WHERE profile_id=%s GROUP BY user_entry_id,review_id,profile_id,`type` ORDER BY profile_id;"""

UNIQUEPIN2 = """SELECT UUID() AS `unique_id`,MIN(pin_id) AS id,user_entry_id,NULL AS review_id,profile_id,`type` FROM vw_user_pin_details WHERE profile_id=%s AND `type` in ('Listing Review','Professional Review') GROUP BY user_entry_id,review_id,profile_id,`type` ORDER BY profile_id;"""

FRIEND_NOT_CONNECTED = """ select distinct A.id, A.profile_id, A.user_id,A.username
                 from
                 ( select ri.id, rip.profile_id, up.id as user_id,au.username 
                   from
                      (
                        select * from reviews_importedcontacts_profile where profile_id=%d
                      ) rip
                       inner join reviews_importedcontacts ri  on rip.importedcontacts_id=ri.id
                       inner join auth_user au on au.email=ri.email
                       inner join users_profile up on au.id=up.user_id
                       LEfT outer join multiuploader_multiuploaderfile mm on mm.id=up.current_profile_pic_id
                       where up.id not in(
                          select connection_id as friend_id from  reviews_connections
                          where profile_id=%d
                          union
                          select profile_id as friend_id from  reviews_connections
                          where connection_id=%d)
                 )A;
                 """

PHONE_TYPE = "FIXED_LINE"


MOVIES_FAVOURITE_CATEGORY = """
                            SELECT DISTINCT ru.id FROM reviews_userentries_taxonomy rut
                            INNER JOIN reviews_userentries ru 
                            ON rut.userentries_id=ru.id AND ru.content_type_id
                            =(SELECT id FROM taxonomy_taxonomy WHERE parent_id=1 AND category='movies')
                            INNER JOIN review_review rr
                            ON ru.id=rr.associated_to_id
                            WHERE rut.taxonomy_id IN %s 
                            ORDER BY ru.movie_release_date DESC limit 25;
                        """
                        
MOVIES_FAVOURITE_SINGLE_CATEGORY = """
                            SELECT DISTINCT ru.id FROM reviews_userentries_taxonomy rut
                            INNER JOIN reviews_userentries ru 
                            ON rut.userentries_id=ru.id AND ru.content_type_id
                            =(SELECT id FROM taxonomy_taxonomy WHERE parent_id=1 AND category='movies')
                            INNER JOIN review_review rr
                            ON ru.id=rr.associated_to_id
                            WHERE rut.taxonomy_id = %s 
                            ORDER BY ru.movie_release_date DESC limit 25;
                        """

PRODUCTS_FAVOURITE_CATEGORY = """
                            SELECT DISTINCT ru.id FROM reviews_userentries_taxonomy rut
                            INNER JOIN reviews_userentries ru 
                            ON rut.userentries_id=ru.id AND ru.content_type_id
                            =(SELECT id FROM taxonomy_taxonomy WHERE parent_id=1 AND category='products')
                            INNER JOIN review_review rr
                            ON ru.id=rr.associated_to_id
                            WHERE rut.taxonomy_id IN %s limit 25;
                         """

PRODUCTS_FAVOURITE_SINGLE_CATEGORY = """
                            SELECT DISTINCT ru.id FROM reviews_userentries_taxonomy rut
                            INNER JOIN reviews_userentries ru 
                            ON rut.userentries_id=ru.id AND ru.content_type_id
                            =(SELECT id FROM taxonomy_taxonomy WHERE parent_id=1 AND category='products')
                            INNER JOIN review_review rr
                            ON ru.id=rr.associated_to_id
                            WHERE rut.taxonomy_id = %s limit 25;
                         """

                         
COUNTRY_CODE = "1"
STRIP_FROM = 1

INVITE_FRIENDS = """
                    SELECT ric.id FROM reviews_importedcontacts ric 
                    INNER JOIN reviews_importedcontacts_profile ricp 
                    ON ricp.importedcontacts_id = ric.id AND
                    ricp.profile_id = %s
                    WHERE ric.email NOT IN (SELECT email FROM auth_user WHERE email IS NOT NULL);
                """
                
IMPORTED_CONTACTS = """
                        SELECT ric.id FROM reviews_importedcontacts ric 
                    INNER JOIN reviews_importedcontacts_profile ricp 
                    ON ricp.importedcontacts_id = ric.id AND
                    ricp.profile_id = %s;
                    """
                
DEFAULT_BUSINESS_FEED_QUERY = """
                select DISTINCT entry.id FROM reviews_userentries entry 
                inner join users_address address on entry.id = address.entries_id  
                inner join reviews_userentries_primary_media media on entry.id = media.user_entries_id
                INNER JOIN review_review rr ON rr.associated_to_id  = entry.id 
                INNER JOIN reviews_userentries_statistics rus ON rus.reviews_userentries_id = entry.id 
                WHERE (3956 * 2 * ASIN(SQRT(POWER(SIN(('%s' - abs(address.latitude)) * pi()/180 / 2), 2) +  COS('%s' * pi()/180 ) * COS(abs(address.latitude) * pi()/180) * POWER(SIN(('%s' - address.longitude) * pi()/180 / 2), 2) ))) < 100 ORDER BY rus.reviews_count DESC,(3956 * 2 * ASIN(SQRT(POWER(SIN(('%s' - abs(address.latitude)) * pi()/180 / 2), 2) +  COS('%s' * pi()/180 ) * COS(abs(address.latitude) * pi()/180) * POWER(SIN(('%s' - address.longitude) * pi()/180 / 2), 2) ))) LIMIT 20;
            """
            
DEFAULT_MOVIE_FEED_QUERY = """
                select DISTINCT entry.id FROM reviews_userentries entry inner join 
                reviews_userentries_primary_media media on entry.id = media.user_entries_id 
                INNER JOIN review_review rr ON rr.associated_to_id = entry.id 
                INNER JOIN reviews_userentries_statistics rus ON rus.reviews_userentries_id = entry.id
                WHERE entry.content_type_id = (SELECT t.id from taxonomy_taxonomy t where t.parent_id = 1 and t.category = 'Movies') 
                ORDER BY rus.reviews_count DESC,rr.created_date_time DESC LIMIT 20;
            """
            
DEFAULT_PRODUCT_FEED_QUERY = """
            select DISTINCT entry.id FROM reviews_userentries entry inner join reviews_userentries_primary_media media on 
            entry.id = media.user_entries_id INNER JOIN review_review rr ON rr.associated_to_id = entry.id INNER JOIN 
            reviews_userentries_statistics rus ON rus.reviews_userentries_id = entry.id 
            WHERE entry.content_type_id = (SELECT t.id from taxonomy_taxonomy t where t.parent_id = 1 and t.category = 'Products') 
            ORDER BY rus.reviews_count DESC,rr.created_date_time DESC LIMIT 20;
            """
            
RESET_PASSWORD_SUBJECT = ("Password reset on  WikiReviews.")
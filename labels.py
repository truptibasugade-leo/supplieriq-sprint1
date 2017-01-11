"""
Purpose: Labels for User Management.
This File contains all the Labels used in User Management to provide
internationalization/localization.

Constraints:
"""
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site
from .constants import (ZIPCODE_MAX_LENGTH, CITY_MAX_LENGTH,
                        STATE_MAX_LENGTH, ADDR_MAX_LENGTH,
                        FIRST_NAME_MAX_LENGTH,
                        LAST_NAME_MAX_LENGTH, USER_NAME_MAX_LENGTH)

LBL_USER = {
    'FIRST_NAME': _('First Name'),
    'LAST_NAME': _('Last Name'),
    'EMAIL': _('Email Address'),
    'DOB': _('Age'),
    'MOBILE_NO': _('Phone Number'),
    'GENDER': _('Gender'),
    'CONFIRM_EMAIL': _('Confirm Email'),
    'RE_EMAIL': _('Re-enter Email'),
    'CAPTCHA': _('Verification Code'),
    'PASSWORD': _('Password'),
    'PSWD_AGAIN': _('Confirm Password'),
    'DATE_BIRTH': _(' Date of Birth'),
    'ZIPCODE': _('Zipcode/Postal code'),
    'TOS': _('I accept<a target="_blank" href="/tos"> Terms of Services,</a> <a target="_blank" href="/policies"> Privacy Policy</a>,<a target="_blank" href="/guidelines"> Guidelines</a>'),    
    'PRESENT_ADDRESS': _('Lives in'),
    'PERMANENT_ADDRESS': _('From'),
    'ADDRESS1': _('Address1'),
    'ADDRESS2': _('Address2'),
    'CITY': _('City'),
    'STATE': _('State'),
    'COUNTRY': _('Country'),
    'ABOUT_ME': _('About Me'),
    'ABOUT_USER': _('About User'),
    'HOME_THEATER': _('Home Theater'),
    'USERNAME': _('User Name'),
    'VIEW_MY_PROFILE':_("Who can see your User's Info and Selections (Wants,Recommends & Favorites)on your profile page?"),
    'WHO_CAN_SEE_MY_PROFILE':_('Who Can See My Profile?'),
    'WHO_CAN_SEE_MY_STUFF':_('Who Can See My Stuff?'),
    'CLAIM_URL':_('Claim your URL'),
    'REVIEWS_SETTING':_('Reviews'),
    'UPDATE_FEED':_('Update My Feed When Someone'),
    'PRIVATE_MESSAGES':_('Who Can Send Me Private Messages ?'),
    'ANONYMOUS_REVIEWS':_('Reviews'),
    'EMAIL_ME_SETTINGS':_('Watchlist Settings'),
    'EMAIL_ME_WHEN_SOMEONE':_('Email me when someone'),
    'EMAIL_FOR_WIKIREVIEWS_HERALD':_('WikiReviews Herald'),
    'WHO_CAN_SEE_FUTURE_STUFF':_('Who can see your future posts?'),
    'LIMIT_AUDIENCE_OLD_POSTS':_('Limit the Audience for Old Posts'),
    'WHO_CAN_CONTACT_ME':_('Who Can Contact Me? '),
    'WHO_CAN_SEND_YOU_FRIEND_REQUEST':_('Who can send you friend requests ?'),
    'WHO_CAN_LOOK_ME_UP':_('Who Can Look Me Up? '),
    'WHO_CAN_LOOK_YOU_UP_USING_EMAIL':_('Who can look you up using the email address you provided? '),
    'WHO_CAN_LOOK_YOU_UP_USING_PHONE':_('Who can look you up using the phone number you provided? '),
    'LINK_SEARCH_ENGINE_TIMELINES':_('Do you want other search engines to link to your public profile?'),
    'LET_OTHER_SEARCHENGINE_LINK_ME':_('Let other search engines link to your public profile'),
    'MY_SETTINGS':'My Settings',
    'TEMPERATURE_SETTING':'Temperature',
    'SYSTEM_OF_MEASUREMENT':'System of Measurement',
    'FOLLOWER SETTINGS' : _('Follower Settings'),
    'WHO_CAN_FOLLOW_ME':_('Who can follow me?'),
    'FOLLOWER_COMMENTS' : _('Follower Comments'),
    'FOLLOWER_NOTIFICATIONS' : _('Follower Notifications'),
    'MYPOST_AND_TAGGING' : _('My Posts Page & Tagging'),
    'WHO_CAN_POST_ON_YOUR_MY_POSTS_PAGE' : _('Who can post on your My Posts Page?'),
    'WHO_CAN_SEE_POSTS_YOUR_TAGGED_IN_ON_YOUR_POSTS_PAGE' : _('Who can see posts your tagged in on your Posts Page?'),
    'WHO_CAN_SEE_WHAT_OTHERS_POST_ON_YOUR_POSTS_PAGE' : _('Who can see what others post on your Posts Page?'),
    'HOW_CAN_I_MANAGE_TAGS_PEOPLE_ADD' : _('How can I manage tags people add?'),
    'POSTS_ALL_MY_REVIEWS_ON_FACEBOOK' : _('Posts all my Reviews on Facebook'),
    'POST_ALL_OF_MY_COMMUNITY_REVIEW_PROJECTS_ON_FACEBOOK' : _('Post all of my Community Review Projects on Facebook'),
    'SHARING' : _('Sharing'),
    'VIDEO_SETTINGS' : _('Video Settings'),
    'AUTO_PLAY_VIDEOS' : _('Auto Play Videos'),
    'VIDEO_DEFAULT_QUALITY' : _('Video Default Quality'),
    'WATCHLIST_NOTIFICATIONS' : _('Watchlist Notifications'),
    'AUTOMATICALLY_ADD_PAGES_I_EDIT_TO_MY_WATCHLIST' : _('Automatically add pages I edit to my Watchlist'),
    'DONT_PUT_MY_OWN_CHANGES_ON_MY_WATCHLIST' : _("Don't put my own changes on my Watchlist"),
    'HOW_YOU_GET_NOTIFICATIONS' : _('How you get notifications '),
    'ON_WIKIREVIEWS' : _('On WikiReviews'),
    'EMAIL' : _('Email'),
    'ALL_NOTIFICATIONS_EXCEPT_ONES_YOU_UNSUBSCRIBE_FROM_BELOW' : _('All notifications, except ones you unsubscribe from below.'),
    'ONLY_NOTIFICATIONS_ABOUT_YOU_YOUR_ACCOUNT_SECURITY_AND_PRIVACY' : _('Only notifications about you, your account, security and privacy.'),
    'SUBSCRIBE_UNSUBSCRIBE_FROM_THE_FOLLOWING' : _('Subscribe/Unsubscribe from the following:'),
    'MESSAGES' : _('Messages'),
    'POSTS_ON_YOUR_MY_POSTS_PAGE' : _('Posts on your My Posts Page'),
    'FRIEND_REQUESTS' : _('Friend Requests'),
    'FRIEND_CONFIRMATIONS' : _('Friend Confirmations'),
    'COMMENTS_ON_VIDEOS_YOU_POSTED' : _('Comments on Videos you posted'),
    'COMMENTS_ON_PHOTOS_YOU_POSTED' : _('Comments on Photos you posted'),
    'COMMENTS_ON_REVIEWS_YOU_POSTED' : _('Comments on reviews you posted'),
    'COMMENTS_ON_ANY_CONTRIBUTION_YOU_MADE' : _('Comments on any contribution you made (tips, warnings, images, video, etc)'),
    'COMMENTS_ON_YOUR_MY_POSTS_PAGE' : _('Comments on your my Posts Page'),
    'THERE_IS_A_COMMENT_ON_A_REVIEW_I_POSTED' : _('There is a comment on a review I posted'),
    'COMMENTS_ON_A_POST_AFTER_I_POST_A_QUESTION_OR_COMMENT' : _('Comments on a post after I post a question or comment'),
    'THE_STATUS_OF_MY_CONTRIBUTIONS' : _('The status of my contributions (approved or reverted)'),
    'NOTIFY_ME_OF_APPROVED_OR_REVERTED_CONTRIBUTIONS' : _('Notify me of Approved or Reverted contributions'),
    'ONLY_NOTIFY_ME_OF_APPROVED_CONTRIBUTIONS' : _('Only notify me of approved contributions'),
    'ONLY_NOTIFY_ME_OF_REVERTED_CONTRIBUTIONS' : _('Only notify me of reverted contributions'),
    'MY_CONTRIBUTIONS_ARE_DONE_BEING_RATED' : _('My contributions are done being rated'),
    'IF_THE_COMMUNITY_FLAGS_ANY_CONTENT_I_UPLOADED' : _('If the community flags any content I uploaded.'),
    'IF_YOU_ARE_NOMINATED_BY_SOMEONE_AS_AN_ADMINISTRATOR' : _('If you are nominated by someone as an Administrator'),
    'IF_YOU_ARE_NOMINATED_BY_SOMEONE_AS_AN_EXPERT' : _('If you are nominated by someone as an Expert'),
    'FRIEND_SUGGESTIONS' : _('Friend Suggestions'),
    'ANSWERS_TO_YOU_COMMUNITY_FORUM_QUESTIONS' : _(' Answers to you Community Forum Questions'),
    'PEOPLE_WHO_YOU_INVITED_TO_JOIN_WIKIREVIEWS' : _('People who you invited to join WikiReviews'),
    'PEOPLE_SHARING_YOUR_CONTRIBUTIONS_POSTS' : _('People sharing your contributions/Posts'),
    'IMAGES' : _('Images'),
    'VIDEO' : _('Video'),
    'REVIEWS' : _('Reviews'),
    'COMMUNITY_REVIEW_PROJECTS' : _('Community Review Projects'),
    'TIPS' : _('Tips'),
    'WARNINGS' : _('Warnings'),
    'CORE_LISTING_INFO' : _('Core listing info'),
    'TECHNICAL_INFO' : _('Technical Info'),
    'ANSWERS_TO_YOUR_QUESTIONS' : _('Answers to your Questions'),
    'BUSINESS_OWNER_FEEDBACK_TO_YOUR_QUESTIONS' : _('Business Owner feedback to your questions '),
    'ADDITIONAL_ANSWERS_TO_A_QUESTION_AFTER_YOUR_ANSWER' : _('Additional answers to a question after your answer.'),
    'ADDITIONAL_QUESTIONS_POSTED_FOR_LISTINGS_YOU_ALREADY_GAVE_ANSWERS' : _('Additional Questions posted for listings you already gave answers.'),
    'NOTIFY_IF_ANY_LISTING_IN_YOUR_SELECTIONS_BECOMES_DISCONTINUED' : _('Notify if any listing in your Selections becomes discontinued, closed, or moved.'),
    'FRIENDS_APPROVING_YOUR_CHECK-INS_WITH_THEM' : _('Friends approving your check-ins with them'),
    'NEW_REVIEW_ON_MY_COMMUNITY_REVIEW_PROJECT' : _('New review on my Community Review Project'),
    'I_AM_CLOSE_TO_RECEIVING_A_CONTRIBUTION_AWARD' : _('I am close to receiving a Contribution Award '),
    'I_RECEIVE_A_NEW_AWARD_OR_BADGE' : _('I receive a new Award or Badge'),
    'MY_FRIENDS_RECEIVE_AN_ICON_OR_BADGE' : _('My friends receive an Icon or Badge'),
    'NOTIFICATIONS_OF_NEW_EDITIONS_OF_WIKIREVIEWS_HERALD' : _('Notifications of New Editions of WikiReviews Herald'),
    'COMMUNITY_FEEDBACK_RATINGS_OF_YOUR_CONTRIBUTIONS' : _('Community Feedback Ratings of your contributions'),
    'NOTIFICATIONS' : _('Notifications'),
    }

PLACEHOLDER_USER = {
    'FIRST_NAME': _('First name'),
    'LAST_NAME': _('Last Name'),
    'EMAIL': _('Your Email Address'),
    'DOB': _('Set your Date of Birth'),
    'MOBILE_NO': _('Enter Phone Number'),
    'GENDER': _('Set Gender'),
    'CONFIRM_EMAIL': _('Confirm Email Address'),
    'RE_EMAIL': _('Re-enter Email'),
    'CAPTCHA': _('Enter the code above here'),
    'PASSWORD': _('Change Your Password'),
    'PSWD_AGAIN': _('Re-enter Password'),
    'ZIPCODE': _('Zipcode/Postal code'),
    'ADDRESS1': _('Address 1'),
    'ADDRESS2': _('Address 2'),
    'CITY': _('City'),
    'STATE': _('State'),
    'ABOUT_ME': _('I am ...'),
    'HOME_THEATER': _('Enter Zip Code or Name of Theater'),
    'VANITY_URL': _('Set Your Vanity Url'),
    'MOBILE_NO': _('123-456-7890'),
    'VERIFICATION_CODE': _('Enter the code'),
    'USERNAME': _('Enter Username'),
    'POSITION':_('Position'),
    }

EMPTY_TEXT_USER = {
    'FIRST_NAME': _('Please provide your first name'),
    'LAST_NAME': _('Please provide your last name'),
    'DOB': _('Please set your birthday'),
    'MOBILE_NO': _('Enter Phone Number'),
    'GENDER': _('Set Gender'),
    'EMAIL': _('You can change your email address from here'),
    'PASSWORD': _('You can reset your password from here'),
    'PRESENT_ADDRESS': _('Please provide your present address'),
    'PERMANENT_ADDRESS': _('Please provide your permanent address'),
    'ABOUT_ME': _('Please tell us about yourself'),
    'HOME_THEATER': _('You can set your favorite theater from here'),
    'VANITY_URL': _('You can set your vanity url from here'),
    'POSITION':_('Please Provide with your Position'),
    'CITY':_('Enter City'),
    'COUNTRY':_('Enter Country'),
    'HOME_THEATRE': _('Set HOME THEATRE')
    }

DOB_HELP_TEXT = _('In accordance with the Children Online Privacy Protection Act of 1998,\
                  we do not collect personal information from users under the age of 13.\
                  Users under 13 should not post personal information anywhere on the site.')

WORK_TITLE = _('Designation')
EDUCATION_TITLE = _("Degree/Course")
WORK_ENTRY = _('Organization')
EDUCATION_ENTRY = _('University/College')

FORGOT_LINK = _("Forgot your password?")
ACTIVATION_LINK = _("Resend Activation Email")

WORK_IS_PRESENT = _("Present")
EDUCATION_IS_PRESENT = _("Pursuing")

USER_ENTRY_PLACEHOLDER = {
                           'work': _("Type/Search Organization"),
                           'education': _("Type/Search University/Institute"),
                           }
TITLE_PLACEHOLDER = {
                           'work': _("Enter the designation"),
                           'education': _("Enter the degree/course "),
                           }

MAXLENGHT_VAR = {
                 'first_name':FIRST_NAME_MAX_LENGTH,
                 'last_name' : LAST_NAME_MAX_LENGTH,
                 'username': USER_NAME_MAX_LENGTH,
                 'address1':ADDR_MAX_LENGTH,
                 'address2':ADDR_MAX_LENGTH,
                 'city':CITY_MAX_LENGTH,
                 'state':STATE_MAX_LENGTH,
                 'about_me':250,
                 'zipcode':ZIPCODE_MAX_LENGTH,
                 'position':50,
                 }
INVITE_EMAIL = _("Enter Comma seperated email address of users.")
CONNECTIONS_ADD = ("Connection's Address")
CONTACT_NUMBER = ("Enter Number for verfication.")


CONTACT_NAME = _("Contact Name")
CONTACT_PHONE = ("Mobile")
PERSON_MANAGING_ACC = _("The person managing this account")
EMAIL_ADDRESS = _("E-mail Address")
SEARCH_LOCAL_OR_NATIONAL = _("Search local or national using the form.")

WORKING_LABEL = _('Currently Here')


SITE_NAME = "http://" + Site.objects.get(id=1).name + '/people/'


REVIEWS_SETTING_DETAILS = _('Your Reviews are displayed publicly by default. Select this option to block users outside your Friends list from following (subscribing to) Your Reviews.')

REVIEWS_ANONYMOUS_DETAILS = _('(Available after first 5 reviews)')




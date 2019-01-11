"""
Definition of models.
"""

# TODO

# help_text: enter help text for all fields requiring an informative description. Note that this value is not HTML-escaped in automatically-generated forms.
# This lets you include HTML in help_text if you so desire. For example: help_text="Please use the following format: <em>YYYY-MM-DD</em>."

# verbose_name: A human-readable name for the field used in field labels. If not specified, Django will infer the default verbose name from the field name.

# default: The default value for the field. This can be a value or a callable object, in which case the object will be called every time a new record is created.

# null: If True, Django will store blank values as NULL in the database for fields where this is appropriate (a CharField will instead store an empty string). The default is False.

# blank: If True, the field is allowed to be blank in your forms. The default is False, which means that Django's form validation will force you to enter a value. 
# This is often used with null=True , because if you're going to allow blank values, you also want the database to be able to represent them appropriately.

# primary_key: If True, sets the current field as the primary key for the model (A primary key is a special database column designated to uniquely identify all the different table records). 
# If no field is specified as the primary key then Django will automatically add a field for this purpose.

# db_index: If True, a database index will be created for this field.

# unique: when unique is True, you don’t need to specify db_index, because unique implies the creation of an index.

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from uuid import uuid4
import datetime

def generateUUID():
    return str(uuid4())

class CustomUser(AbstractUser):

    user_dfe_number = models.PositiveIntegerField(blank=True) # setting users only, can be more than one setting user for each dfe number
    user_la_code = models.CharField(max_length=9, blank=True) # la users only
    USER_TYPE_CHOICES = (
        ('sft', 'Secure File Transfer user'),
        ('setting', 'Setting user'),
        ('LA', 'Local Authority user'),
        ('admin', 'administrator'),
        ('super', 'super user'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    # is_sft_user = models.BooleanField(default=False)
    # is_setting_user = models.BooleanField(default=False)
    # is_la_user = models.BooleanField(default=False)
    # is_super_user = models.BooleanField(default=False)

    class Meta: 
        ordering = ['user_email']

    def __unicode__(self):
        return f"{self.user_email}"

    def __str__(self):
        return unicode(self).encode('utf-8')

class DistributionList():

    distributionlist_name = models.CharField(max_length=30, primary_key=True)
    distributionlist_description = models.CharField(max_length=100, blank=True)

    class Meta: 
        ordering = ['distributionlist_name']

    def __unicode__(self):
        return f"{self.distributionlist_name}"

    def __str__(self):
        return unicode(self).encode('utf-8')

class MemberOf():

    distributionlist_id = models.ForeignKey('DistributionList', on_delete=models.CASCADE)
    customuser_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE)

class TransferFile():

    file_name = models.CharField(max_length=100)
    encrypted_file_name = models.UUIDField(primary_key=False, default=generateUUID(), editable=False)
    FILE_TYPE_CHOICES = (
        ('xml', 'XML'),
        ('xsn', 'Microsoft InfoPath Form'),
        ('xls', 'Microsoft Excel'),
        ('doc', 'Microsoft Word'),
        ('pdf', 'Adobe Acrobat Reader'),
        ('csv', 'Comma Separated Values'),
        ('txt', 'Plain Text'),
        ('img', 'Image'),
        ('vid', 'Video')
    )
    file_type = models.CharField(max_length=3, choices=FILE_TYPE_CHOICES)

    class Meta: 
        ordering = ['file_name']

    def __unicode__(self):
        return f"{self.file_name}"

    def __str__(self):
        return unicode(self).encode('utf-8')

class FilesSent():

    sender_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    recipient_id = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    file_id = models.ForeignKey('TransferFile', on_delete=models.CASCADE)
    upload_date = models.DateField()
    download_date = models.DateField()

class Term(models.Model):

    term_name = models.CharField(max_length=50)
    term_start_date = models.DateField()
    term_end_date = models.DateField()
    collection_date = models.DateField(help_text='The Monday of Census week')
    dob_min_date = models.DateField()
    dob_max_date = models.DateField()

    class Meta: 
        ordering = ['term_name']

    def __unicode__(self):
        return f"{self.term_name}"

    def __str__(self):
        return unicode(self).encode('utf-8')

class FundingStream(models.Model):

    funding_term_id = models.ForeignKey('Term', on_delete=models.CASCADE)
    FUNDING_TYPE_CHOICES = (
        ('TYF', 'Two year old funding'),
        ('SFF30H', '3 & 4 year old universal and extended entitlement')
    )     
    funding_type = models.CharField(max_length=6, choices=FUNDING_TYPE_CHOICES)
    funding_weeks = models.PositiveSmallIntegerField()
    funding_min_dob = models.DateField()
    funding_max_dob = models.DateField()

class FeeScale(models.Model):

    fee_funding_stream_id = models.ForeignKey('FundingStream', on_delete=models.CASCADE)
    fee_dfe_id = models.PositiveIntegerField(blank=True) # not set for TYF
    fee_setting_name = models.CharField(max_length=100, blank=True) # not set for TYF
    fee_per_hour = models.DecimalField(max_digits=4, decimal_places=2)

    class Meta: 
        ordering = ['fee_setting_name']

class Setting(models.Model):

    setting_name = models.CharField(max_length=100)
    setting_address_1 = models.CharField(max_length=100)
    setting_address_2 = models.CharField(max_length=100, blank=True)
    setting_address_3 = models.CharField(max_length=100, blank=True)
    setting_address_4 = models.CharField(max_length=100, blank=True)
    setting_address_5 = models.CharField(max_length=100, blank=True)
    setting_postcode = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex='^[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2}$',
                message='Postcode is not a recognizable format',
                code='invalid_postcode'
            ),
        ]
    )
    setting_email_address = models.EmailField()
    manager_title = models.CharField(max_length=10)
    manager_first_name = models.CharField(max_length=100)
    manager_last_name = models.CharField(max_length=100)
    manager_mobile_number = models.CharField(
        max_length=14,
        blank=True,
        validators=[
            RegexValidator(
                regex='^(07[\d]{8,12}|447[\d]{7,11})$',
                message='Mobile number is not a recognizable format',
                code='invalid_mobile_number'
            ),
        ]
    )
    manager_email_address = models.EmailField(blank=True)
    setting_dfe_urn = models.PositiveIntegerField()
    setting_ofsted_urn = models.CharField(max_length=10)
    setting_ofsted_outcome_date = models.DateField(default=datetime.date(9999,1,1))
    OFSTED_OUTCOME_CHOICES = (
        ('Not Inspected Yet', 'Not Inspected Yet'),
        ('Outstanding', 'Outstanding'),
        ('Good', 'Good'),
        ('Met', 'Met'),
        ('Not Met', 'Not Met'),
        ('Requires Improvement', 'Requires Improvement'),
        ('Inadequate', 'Inadequate')
    )
    setting_ofsted_outcome = models.CharField(max_length=20, choices=OFSTED_OUTCOME_CHOICES)
    SETTING_CATEGORY_CHOICES = (
        ('CHMD', (
                ('AGY', 'Part of Childminding Agency'),
                ('IND', 'Individual Childminder')
            )
        ),
        ('INDS', 'Registered Independent School'),
        ('LADN', 'Local Authority Day Nursery'),
        ('OTHR', 'Other'),
        ('PRIV', 'Private'),
        ('VOLY', 'Voluntary')
    )    
    setting_category = models.CharField(max_length=4, choices=SETTING_CATEGORY_CHOICES)
    SETTING_TYPE_CHOICES = (
        ('DNS', 'Day Nursery'),
        ('PPS', 'Playgroup or Pre-school'),
        ('NUR', 'Nursery school'),
        ('FCI', 'Family or Combined or Integrated Centre'),
        ('SSM', 'Sure Start Children\'s Centre'),
        ('SSL', 'Satelite Sure Start Children\'s Centre'),
        ('OTH', 'Other')
    )    
    setting_type = models.CharField(max_length=3, choices=SETTING_TYPE_CHOICES)
    SETTING_DAYCARE_CHOICES = (
        ('F', 'Full day (6 hours or more)'),
        ('S', 'Sessional day (less than 6 hours)'),
        ('O', 'Other day care')
    )    
    setting_daycare_type = models.CharField(max_length=1, choices=SETTING_DAYCARE_CHOICES)
    setting_continuously_open = models.BooleanField(default=False, help_text='Open 24 hours a day, 7 days per week')
    setting_school_relationship = models.BooleanField(default=False)
    setting_establishment_partnership = models.BooleanField(default=False)
    setting_weeks_per_year_open = models.DecimalField(max_digits=3, decimal_places=1, default=38.0)
    setting_total_teaching_staff = models.PositiveSmallIntegerField()
    setting_level2_staff = models.PositiveSmallIntegerField()
    setting_level3_staff_not_management = models.PositiveSmallIntegerField()
    setting_level3_staff_management = models.PositiveSmallIntegerField()
    setting_qts_staff = models.PositiveSmallIntegerField()
    setting_eyps_staff = models.PositiveSmallIntegerField()
    setting_eyts_staff = models.PositiveSmallIntegerField()

    class Meta: 
        ordering = ['setting_name']

    def __unicode__(self):
        return f"{self.setting_name}"

    def __str__(self):
        return unicode(self).encode('utf-8')

class SettingDay(models.Model):

    day_setting_id = models.ForeignKey('Setting', on_delete=models.CASCADE)
    DAYS_OF_WEEK = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday')
    )
    day_of_week = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK)
    day_opening_time = models.TimeField(default=datetime.time(00, 00))
    day_lunch_period = models.TimeField(default=datetime.time(00, 00))
    day_closing_time = models.TimeField(default=datetime.time(00, 00))
    day_under_two_capacity = models.PositiveSmallIntegerField(default=0)
    day_two_capacity = models.PositiveSmallIntegerField(default=0)
    day_over_two_capacity = models.PositiveSmallIntegerField(default=0)

class SettingFee(models.Model):

    fee_setting_id = models.ForeignKey('Setting', on_delete=models.CASCADE)
    FEE_GROUP = (
        ('F', 'Weekly Fixed'),
        ('U2', 'Under Two Year Old'),
        ('2', 'Two Year Old'),
        ('O2', 'Over Two Year Old')
    )
    fee_group = models.CharField(max_length=2, choices=FEE_GROUP)
    fee_hours = models.DecimalField(max_digits=3, decimal_places=2)
    fee_amount = models.DecimalField(max_digits=5, decimal_places=2)

class Pupil(models.Model):

    pupil_setting_id = models.ForeignKey('Setting', on_delete=models.CASCADE)
    pupil_first_name = models.CharField(max_length=100)
    pupil_last_name = models.CharField(max_length=100)
    pupil_address_1 = models.CharField(max_length=100)
    pupil_address_2 = models.CharField(max_length=100, blank=True)
    pupil_address_3 = models.CharField(max_length=100, blank=True)
    pupil_address_4 = models.CharField(max_length=100, blank=True)
    pupil_address_5 = models.CharField(max_length=100, blank=True)
    pupil_postcode = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex='^[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2}$',
                message='Postcode is not a recognizable format',
                code='invalid_postcode'
            ),
        ]
    )
    pupil_dob = models.DateField()
    GENDER = (
        ('1', 'Male'),
        ('2', 'Female'),
        ('9', 'Not Specified')
       )
    pupil_gender = models.CharField(max_length=1, choices=GENDER)
    ETHNICITY = (
        ('WBRI', (
                ('WCOR', 'White - Cornish'),
                ('WENG', 'White - English'),
                ('WSCO', 'White - Scottish'),
                ('WWEL', 'White - Welsh'),
                ('WOWB', 'Other White British')
            )
         ),
        ('WIRI', 'White - Irish'),
        ('WIRT', 'Traveller of Irish heritage'),
        ('WOTH', (
                ('WALB', 'Albanian'),
                ('WBOS', 'Bosnian- Herzegovinian'),
                ('WCRO', 'Croatian'),
                ('WGRE', 'Greek/ Greek Cypriot'),
                ('WGRK', 'Greek'),
                ('WGRC', 'Greek Cypriot'),
                ('WITA', 'Italian'),
                ('WKOS', 'Kosovan'),
                ('WPOR', 'Portuguese'),
                ('WSER', 'Serbian'),
                ('WTUR', 'Turkish/Turkish Cypriot'),
                ('WTUK', 'Turkish'),
                ('WTUC', 'Turkish Cypriot'),
                ('WEUR', 'White European'),
                ('WEEU', 'White Eastern European'),
                ('WWEU', 'White Western European'),
                ('WOTW', 'White other')
            )
         ),
        ('WROM', (
                ('WROG', 'Gypsy'),
                ('WROR', 'Roma'),
                ('WROO', 'Other Gypsy/Roma')
            )
         ),
        ('MWBC', 'White and Black Caribbean'),
        ('MWBA', 'White and Black African'),
        ('MWAS', (
                ('MWAP', 'White and Pakistani'),
                ('MWAI', 'White and Indian'),
                ('MWAO', 'White and any other Asian background')
            )
         ),
        ('MOTH', (
                ('MAOE', 'Asian and any other ethnic group'),
                ('MABL', 'Asian and Black'),
                ('MACH', 'Asian and Chinese'),
                ('MBOE', 'Black and any other ethnic group'),
                ('MBCH', 'Black and Chinese'),
                ('MCOE', 'Chinese and any other ethnic group'),
                ('MWOE', 'White and any other ethnic group'),
                ('MWCH', 'White and Chinese'),
                ('MOTM', 'Other mixed background')
            )
         ),
        ('AIND', 'Indian'),
        ('APKN', (
                ('AMPK', 'Mirpuri Pakistani'),
                ('AKPA', 'Kashmiri Pakistani'),
                ('AOPK', 'Other Pakistani')
            )
         ),
        ('ABAN', 'Bangladeshi'),
        ('AOTH', (
                ('AAFR', 'African Asian'),
                ('AKAO', 'Kashmiri other'),
                ('ANEP', 'Nepali'),
                ('ASNL', 'Sri Lankan Sinhalese'),
                ('ASLT', 'Sri Lankan Tamil'),
                ('ASRO', 'Sri Lankan other'),
                ('AOTA', 'Other Asian')
            )
         ),
        ('BCRB', 'Black Caribbean'),
        ('BAFR', (
                ('BANN', 'Black - Angolan'),
                ('BCON', 'Black - Congolese'),
                ('BGHA', 'Black - Ghanaian'),
                ('BNGN', 'Black - Nigerian'),
                ('BSLN', 'Black - Sierra Leonean'),
                ('BSOM', 'Black - Somali'),
                ('BSUD', 'Black - Sudanese'),
                ('BAOF', 'Other Black African')
            )
         ),
        ('BOTH', (
                ('BEUR', 'Black European'),
                ('BNAM', 'Black North American'),
                ('BOTB', 'Other Black')
            )
         ),
        ('CHNE', (
                ('CHKC', 'Hong Kong Chinese'),
                ('CMAL', 'Malaysian Chinese'),
                ('CSNG', 'Singaporean Chinese'),
                ('CTWN', 'Taiwanese'),
                ('COCH', '')
            )
         ),
        ('OOTH', (
                ('OAFG', 'Afghan'),
                ('OARA', 'Arab other'),
                ('OEGY', 'Egyptian'),
                ('OFIL', 'Filipino'),
                ('OIRN', 'Iranian'),
                ('OIRQ', 'Iraqi'),
                ('OJPN', 'Japanese'),
                ('OKOR', 'Korean'),
                ('OKRD', 'Kurdish'),
                ('OLAM', 'Latin/South/Central American'),
                ('OLEB', 'Lebanese'),
                ('OLIB', 'Libyan'),
                ('OMAL', 'Malay'),
                ('OMRC', 'Moroccan'),
                ('OPOL', 'Polynesian'),
                ('OTHA', 'Thai'),
                ('OVIE', 'Vietnamese'),
                ('OYEM', 'Yemeni'),
                ('OOEG', 'Other ethnic group')
            )
         ),
        ('REFU', 'Refused'),
        ('NOBT', 'Information not yet obtained')
    )
    pupil_ethnicity = models.CharField(max_length=4, choices=ETHNICITY)
    SEN_PROVISION = (
        ('N', 'No special educational need'),
        ('S', 'Statement'),
        ('E', 'Education, health and care plan'),
        ('K', 'SEN support')
    )
    pupil_sen = models.CharField(max_length=1, choices=SEN_PROVISION, default='N')
    pupil_daf = models.BooleanField(default=False)
    pupil_start_date = models.DateField()
    pupil_finish_date = models.DateField(default=datetime.date(9999,1,1))
    pupil_tyo_start_date = models.DateField(default=datetime.date(9999,1,1))
    pupil_tyo_finish_date = models.DateField(default=datetime.date(9999,1,1))
    pupil_sff_start_date = models.DateField(default=datetime.date(9999,1,1))
    pupil_sff_finish_date = models.DateField(default=datetime.date(9999,1,1))
    pupil_30h_start_date = models.DateField(default=datetime.date(9999,1,1))
    pupil_30h_finish_date = models.DateField(default=datetime.date(9999,1,1))
    pupil_30h_grace_period = models.DateField(default=datetime.date(9999,1,1))
    pupil_total_hours = models.DecimalField(max_digits=4, decimal_places=2) # derived field: session_hours mon - sun
    pupil_total_tyf_hours = models.DecimalField(max_digits=4, decimal_places=2) # derived field: session_tyf_hours: mon + tue + wed + thu + fri + sat + sun
    pupil_total_sff_hours = models.DecimalField(max_digits=4, decimal_places=2) # derived field: session_sff_hours: mon + tue + wed + thu + fri + sat + sun
    pupil_total_30h_hours = models.DecimalField(max_digits=4, decimal_places=2) # derived field: session_30h_hours: mon + tue + wed + thu + fri + sat + sun
    pupil_total_funded_hours = models.DecimalField(max_digits=4, decimal_places=2) # derived field: session_funded_hours: mon + tue + wed + thu + fri + sat + sun
    pupil_notes = models.TextField(blank=True)
    pupil_parent_name = models.CharField(max_length=100, blank=True)
    pupil_parent_dob = models.DateField(default=datetime.date(9999,1,1))
    pupil_parent_nino = models.CharField(
        max_length=9,
        default=None,
        validators=[
            RegexValidator(
                regex='^[ABCEGHJKLMNOPRSTWXYZ][ABCEGHJKLMNPRSTWXYZ][0-9]{6}[A-D ]$',
                message='National Insurance number is not a recognizable format',
                code='invalid_nino'
            ),
        ]
    )
    EYPP_STATUS = (
        ('Not Applicable', 'Not Applicable'),
        ('Parent Declined', 'Parent Declined'),
        ('Incomplete data', 'Incomplete data'),
        ('Submit', 'Submit'),
        ('Ineligible', 'Ineligible'),
        ('Eligible', 'Eligible')
    )
    eypp_status = models.CharField(max_length=15, choices=EYPP_STATUS)
    eypp_check_date = models.DateField(default=datetime.date(9999,1,1))
    eypp_outcome = models.BooleanField(blank=True)
    tyf_reference = models.CharField(
        max_length=17,
        blank=True,
        validators=[
            RegexValidator(
                regex='^TYF-[0-9]{4}-[A-Z0-9]{8}$',
                message='TYF is not a recognizable format',
                code='invalid_tyf'
            ),
        ]
    )
    TYF_STATUS = (
        ('Not Applicable', 'Not Applicable'),
        ('TYOF not claimed', 'TYOF not claimed'),
        ('Invalid TYOF format', 'Invalid TYOF format'),
        ('TYOF Reference not found on the Portal', 'TYOF Reference not found on the Portal'),
        ('Eligibility dates not eligible for this term', 'Eligibility dates not eligible for this term'),
        ('Sumitted and portal forenames are different', 'Sumitted and portal forenames are different'),
        ('Sumitted and portal surnames are different', 'Sumitted and portal surnames are different'),
        ('Submitted tyf start date precedes the eligibility start date', 'Submitted tyf start date precedes the eligibility start date'),
        ('Eligible', 'Eligible')
    )
    tyf_status = models.CharField(max_length=100, choices=TYF_STATUS, blank=True)
    tyf_portal_forename = models.CharField(max_length=100, blank=True)
    tyf_portal_surname = models.CharField(max_length=100, blank=True)
    tyf_portal_dob = models.DateField(default=datetime.date(9999,1,1))
    TYF_FUNDING_BASIS = (
        ('ECO', 'Economic criteria'),
        ('HSD', 'High-level SEN or disability'),
        ('LAA', 'Looked after or adopted from care')
    )
    tyf_basis_for_funding = models.CharField(max_length=3, choices=TYF_FUNDING_BASIS, blank=True)
    thirty_hours_dern = models.PositiveIntegerField(
        blank=True,
        validators=[
            RegexValidator(
                regex='^[1-9][0-9]{10}$',
                message='DERN is not a recognizable format',
                code='invalid_dern'
            ),
        ]
    )
    DERN_STATUS = (
        ('Invalid DERN', 'Invalid DERN'),
        ('Missing DERN', 'Missing DERN'),
        ('DERN not found', 'DERN not found'),
        ('30H not claimed', '30H not claimed'),
        ('DoB out of range', 'DoB out of range'),
        ('Child DoB does not match DoB on portal', 'Child DoB does not match DoB on portal'),
        ('Invalid date format', 'Invalid date format'),
        ('No Dates found on the Portal', 'No Dates found on the Portal'),
        ('Beyond Grace Period on Portal', 'Beyond Grace Period on Portal'),
        ('Eligible', 'Eligible')
    )
    thirty_hours_dern_status = models.CharField(max_length=100, choices=DERN_STATUS, blank=True)
    thirty_hours_portal_forename = models.CharField(max_length=100, blank=True)
    thirty_hours_portal_surname = models.CharField(max_length=100, blank=True)
    thirty_hours_portal_dob = models.DateField(default=datetime.date(9999,1,1))

    class Meta: 
        ordering = ['pupil_last_name', 'pupil_first_name']

    def __unicode__(self):
        return f"{self.pupil_last_name} {self.pupil_first_name} {self.pupil_dob}"

    def __str__(self):
        return unicode(self).encode('utf-8')

class PupilSessions(models.Model):

    session_pupil_id = models.ForeignKey('Pupil', on_delete=models.CASCADE)
    DAYS_OF_WEEK = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday')
    )
    session_day_of_week = models.PositiveSmallIntegerField(choices=DAYS_OF_WEEK)
    session_start_time = models.TimeField(default=datetime.time(00, 00))
    session_finish_time = models.TimeField(default=datetime.time(00, 00))
    session_hours = models.DecimalField(max_digits=4, decimal_places=2) # derived field: session_finish_time - session_start_time
    session_tyf_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    session_sff_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    session_30h_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    session_funded_hours = models.DecimalField(max_digits=4, decimal_places=2) # derived field: session_tyf_hours + session_sff_hours + session_30h_hours

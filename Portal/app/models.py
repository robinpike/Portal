"""
Definition of models.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
import datetime

class User(AbstractUser):

    is_sft_user = models.BooleanField(default=False)
    is_setting_user = models.BooleanField(default=False)
    is_la_user = models.BooleanField(default=False)
    is_super_user = models.BooleanField(default=False)
    dfe_number = models.PositiveIntegerField() # setting users only, can be more than one setting user for each dfe number
    la_code = models.CharField(max_length=9) # la users only

    def __unicode__(self):
        return self.text

class Group():

    group_name = models.CharField(max_length=30)
    group_description = models.CharField(max_length=100)

    def __unicode__(self):
        return self.text

class Membership():

    user = models.ManyToManyField(User)
    group = models.ManyToManyField(Group)
    # user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)

    def __unicode__(self):
        return self.text

class Files():

    file_name = models.CharField(max_length=100)
    encrypted_file_name = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
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

    def __unicode__(self):
        return self.text

class FilesSent():

    sender = models.ManyToManyField(User)
    recipient = models.ManyToManyField(User)
    # sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    # recipient = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    upload_date = models.DateField()
    download_date = models.DateField()

    def __unicode__(self):
        return self.text
    
class Term(models.Model):

    term_name = models.CharField(max_length=50)
    term_start_date = models.DateField()
    term_end_date = models.DateField()
    collection_date = models.DateField()
    dob_min_date = models.DateField()
    dob_max_date = models.DateField()

    def __unicode__(self):
        return self.text

class FundingStream(models.Model):

    funding_term = models.ForeignKey(Term, on_delete=models.CASCADE)
    funding_type = models.CharField(max_length=3)
    funding_weeks = models.PositiveSmallIntegerField()
    funding_min_dob = models.DateField()
    funding_max_dob = models.DateField()

    def __unicode__(self):
        return self.text

class FeeScale(models.Model):

    fee_funding_type = models.ForeignKey(FundingStream, on_delete=models.CASCADE)
    fee_dfe_id = models.PositiveIntegerField()
    fee_setting = models.CharField(max_length=100)
    fee_per_hour = models.DecimalField(max_digits=4, decimal_places=2)

    def __unicode__(self):
        return self.text

class Setting(models.Model):

    setting_name = models.CharField(max_length=100) # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
    setting_address_1 = models.CharField(max_length=100) # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
    setting_address_2 = models.CharField(max_length=100)
    setting_address_3 = models.CharField(max_length=100)
    setting_address_4 = models.CharField(max_length=100)
    setting_address_5 = models.CharField(max_length=100)
    setting_postcode = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex='^[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2}$',
                message='Postcode is not a recognizable format',
                code='invalid_postcode'
            ),
        ]
    ) # required=True, produces TypeError: __init__() got an unexpected keyword argument 'required'
    setting_phone_number = models.CharField(max_length=20)  # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
    setting_email_address = models.EmailField()  # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
    manager_title = models.CharField(max_length=10)  # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
    manager_first_name = models.CharField(max_length=100)  # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
    manager_last_name = models.CharField(max_length=100)  # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
    manager_mobile_number = models.CharField(
        max_length=14,
        validators=[
            RegexValidator(
                regex='^(07[\d]{8,12}|447[\d]{7,11})$',
                message='Mobile number is not a recognizable format',
                code='invalid_mobile_number'
            ),
        ]
    )
    manager_email_address = models.EmailField()
    setting_dfe_urn = models.PositiveIntegerField()  # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
    setting_ofsted_urn = models.CharField(max_length=10)  # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
    setting_ofsted_outcome_date = models.DateField()  # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
    OFSTED_OUTCOME_CHOICES = (
        ('Not Inspected Yet', 'Not Inspected Yet'),
        ('Outstanding', 'Outstanding'),
        ('Good', 'Good'),
        ('Met', 'Met'),
        ('Not Met', 'Not Met'),
        ('Requires Improvement', 'Requires Improvement'),
        ('Inadequate', 'Inadequate')
    )
    setting_ofsted_outcome = models.CharField(max_length=20, choices=OFSTED_OUTCOME_CHOICES)  # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
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
    setting_category = models.CharField(max_length=4, choices=SETTING_CATEGORY_CHOICES)  # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
    SETTING_TYPE_CHOICES = (
        ('DNS', 'Day Nursery'),
        ('PPS', 'Playgroup or Pre-school'),
        ('NUR', 'Nursery school'),
        ('FCI', 'Family or Combined or Integrated Centre'),
        ('SSM', 'Sure Start Children\'s Centre'),
        ('SSL', 'Satelite Sure Start Children\'s Centre'),
        ('OTH', 'Other')
    )    
    setting_type = models.CharField(max_length=3, choices=SETTING_TYPE_CHOICES)  # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
    SETTING_DAYCARE_CHOICES = (
        ('F', 'Full day (6 hours or more)'),
        ('S', 'Sessional day (less than 6 hours)'),
        ('O', 'Other day care')
    )    
    setting_daycare_type = models.CharField(max_length=1, choices=SETTING_DAYCARE_CHOICES)  # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
    setting_continuously_open = models.BooleanField()  # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
    setting_school_relationship = models.BooleanField()  # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
    setting_establishment_partnership = models.BooleanField()  # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
    setting_weeks_per_year_open = models.DecimalField(max_digits=3, decimal_places=1, default=38.0)  # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
    setting_total_teaching_staff = models.PositiveSmallIntegerField()
    setting_level2_staff = models.PositiveSmallIntegerField()
    setting_level3_staff_not_management = models.PositiveSmallIntegerField()
    setting_level3_staff_management = models.PositiveSmallIntegerField()
    setting_qts_staff = models.PositiveSmallIntegerField()
    setting_eyps_staff = models.PositiveSmallIntegerField()
    setting_eyts_staff = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return self.text

class SettingDay(models.Model):

    day_setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
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

    def __unicode__(self):
        return self.text

class SettingFees(models.Model):

    fees_setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    FEE_GROUP = (
        ('F', 'Weekly Fixed'),
        ('U2', 'Under Two Year Old'),
        ('2', 'Two Year Old'),
        ('O2', 'Over Two Year Old')
    )
    fees_group = models.CharField(max_length=2, choices=FEE_GROUP)
    fees_hours = models.DecimalField(max_digits=3, decimal_places=2)
    fees_amount = models.DecimalField(max_digits=5, decimal_places=2)

    def __unicode__(self):
        return self.text

class Pupil(models.Model):

    pupil_setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    pupil_first_name = models.CharField(max_length=100) # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
    pupil_last_name = models.CharField(max_length=100) # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
    pupil_address_1 = models.CharField(max_length=100) # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
    pupil_address_2 = models.CharField(max_length=100)
    pupil_address_3 = models.CharField(max_length=100)
    pupil_address_4 = models.CharField(max_length=100)
    pupil_address_5 = models.CharField(max_length=100)
    pupil_postcode = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex='^[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2}$',
                message='Postcode is not a recognizable format',
                code='invalid_postcode'
            ),
        ]
    ) # required=True, produces TypeError: __init__() got an unexpected keyword argument 'required'
    pupil_dob = models.DateField() # required=True produces TypeError: __init__() got an unexpected keyword argument 'required'
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
    pupil_sen = models.CharField(max_length=1, choices=SEN_PROVISION)
    pupil_daf = models.BooleanField()
    pupil_start_date = models.DateField()
    pupil_finish_date = models.DateField()
    pupil_tyo_start_date = models.DateField()
    pupil_tyo_finish_date = models.DateField()
    pupil_sff_start_date = models.DateField()
    pupil_sff_finish_date = models.DateField()
    pupil_30h_start_date = models.DateField()
    pupil_30h_finish_date = models.DateField()
    pupil_30h_grace_period = models.DateField()
    pupil_total_hours = models.DecimalField(max_digits=4, decimal_places=2) # derived field: session_hours mon - sun
    pupil_total_tyf_hours = models.DecimalField(max_digits=4, decimal_places=2) # derived field: session_tyf_hours: mon + tue + wed + thu + fri + sat + sun
    pupil_total_sff_hours = models.DecimalField(max_digits=4, decimal_places=2) # derived field: session_sff_hours: mon + tue + wed + thu + fri + sat + sun
    pupil_total_30h_hours = models.DecimalField(max_digits=4, decimal_places=2) # derived field: session_30h_hours: mon + tue + wed + thu + fri + sat + sun
    pupil_total_funded_hours = models.DecimalField(max_digits=4, decimal_places=2) # derived field: session_funded_hours: mon + tue + wed + thu + fri + sat + sun
    pupil_notes = models.TextField()
    pupil_parent_name = models.CharField(max_length=100)
    pupil_parent_dob = models.DateField()
    pupil_parent_nino = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(
                regex='^[ABCEGHJKLMNOPRSTWXYZ][ABCEGHJKLMNPRSTWXYZ][0-9]{6}[A-D ]$',
                message='National Insurance number is not a recognizable format',
                code='invalid_nino'
            ),
        ]
    )
    EYPP_STATUS = (
        ('Parent Declined', 'Parent Declined'),
        ('Incomplete data', 'Incomplete data'),
        ('Submit', 'Submit'),
        ('Ineligible', 'Ineligible'),
        ('Eligible', 'Eligible')
    )
    eypp_status = models.CharField(max_length=15, choices=EYPP_STATUS)
    eypp_check_date = models.DateField()
    eypp_outcome = models.BooleanField()
    tyf_reference = models.CharField(
        max_length=17,
        validators=[
            RegexValidator(
                regex='^TYF-[0-9]{4}-[A-Z0-9]{8}$',
                message='TYF is not a recognizable format',
                code='invalid_tyf'
            ),
        ]
    )
    TYF_STATUS = (
        ('TYOF not claimed', 'TYOF not claimed'),
        ('Invalid TYOF format', 'Invalid TYOF format'),
        ('TYOF Reference not found on the Portal', 'TYOF Reference not found on the Portal'),
        ('Eligibility dates not eligible for this term', 'Eligibility dates not eligible for this term'),
        ('Sumitted and portal forenames are different', 'Sumitted and portal forenames are different'),
        ('Sumitted and portal surnames are different', 'Sumitted and portal surnames are different'),
        ('Submitted tyf start date precedes the eligibility start date', 'Submitted tyf start date precedes the eligibility start date'),
        ('Eligible', 'Eligible')
    )
    tyf_status = models.CharField(max_length=100, choices=TYF_STATUS)
    tyf_portal_forename = models.CharField(max_length=100)
    tyf_portal_surname = models.CharField(max_length=100)
    tyf_portal_dob = models.DateField()
    TYF_FUNDING_BASIS = (
        ('ECO', 'Economic criteria'),
        ('HSD', 'High-level SEN or disability'),
        ('LAA', 'Looked after or adopted from care')
    )
    tyf_basis_for_funding = models.CharField(max_length=3, choices=TYF_FUNDING_BASIS)
    thirty_hours_dern = models.PositiveIntegerField(
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
    thirty_hours_dern_status = models.CharField(max_length=100, choices=DERN_STATUS)
    thirty_hours_portal_forename = models.CharField(max_length=100)
    thirty_hours_portal_surname = models.CharField(max_length=100)
    thirty_hours_portal_dob = models.DateField()


    def __unicode__(self):
        return self.text

class Pupil_Sessions(models.Model):

    session_pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE)
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
    session_tyf_hours = models.DecimalField(max_digits=4, decimal_places=2)
    session_sff_hours = models.DecimalField(max_digits=4, decimal_places=2)
    session_30h_hours = models.DecimalField(max_digits=4, decimal_places=2)
    session_funded_hours = models.DecimalField(max_digits=4, decimal_places=2) # derived field: session_tyf_hours + session_sff_hours + session_30h_hours

    def __unicode__(self):
        return self.text

"""
Definition of models.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class User(AbstractUser):

    is_setting_user = models.BooleanField(default=False)
    is_la_user = models.BooleanField(default=False)
    is_super_user = models.BooleanField(default=False)

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

    setting_name = models.CharField(max_length=100, required=True)
    setting_address_1 = models.CharField(max_length=100, required=True)
    setting_address_2 = models.CharField(max_length=100)
    setting_address_3 = models.CharField(max_length=100)
    setting_address_4 = models.CharField(max_length=100)
    setting_address_5 = models.CharField(max_length=100)
    setting_postcode = models.CharField(
        max_length=8,
        required=True,
        validators=[
            RegexValidator(
                regex='^[A-Z]{1,2}[0-9R][0-9A-Z]? [0-9][A-Z]{2}$',
                message='Postcode is not a recognizable format',
                code='invalid_postcode'
            ),
        ]
    )
    setting_phone_number = models.CharField(max_length=20, required=True)
    setting_email_address = models.EmailField(required=True)
    manager_title = models.CharField(max_length=10, required=True)
    manager_first_name = models.CharField(max_length=100, required=True)
    manager_last_name = models.CharField(max_length=100, required=True)
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
    setting_dfe_urn = models.PositiveIntegerField(required=True)
    setting_ofsted_urn = models.CharField(max_length=10, required=True)
    setting_ofsted_outcome_date = models.DateField(required=True)
    OFSTED_OUTCOME_CHOICES = (
        ('Not Inspected Yet', 'Not Inspected Yet'),
        ('Outstanding', 'Outstanding'),
        ('Good', 'Good'),
        ('Met', 'Met'),
        ('Not Met', 'Not Met'),
        ('Requires Improvement', 'Requires Improvement'),
        ('Inadequate', 'Inadequate')
    )
    setting_ofsted_outcome = models.CharField(max_length=20, choices=OFSTED_OUTCOME_CHOICES, required=True)
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
    setting_category = models.CharField(max_length=4, choices=SETTING_CATEGORY_CHOICES, required=True)
    SETTING_TYPE_CHOICES = (
        ('DNS', 'Day Nursery'),
        ('PPS', 'Playgroup or Pre-school'),
        ('NUR', 'Nursery school'),
        ('FCI', 'Family or Combined or Integrated Centre'),
        ('SSM', 'Sure Start Children\'s Centre'),
        ('SSL', 'Satelite Sure Start Children\'s Centre'),
        ('OTH', 'Other')
    )    
    setting_type = models.CharField(max_length=3, choices=SETTING_TYPE_CHOICES, required=True)
    SETTING_DAYCARE_CHOICES = (
        ('F', 'Full Daycare'),
        ('S', 'Sessional Daycare'),
        ('O', 'Other Daycare')
    )    
    setting_daycare_type = models.CharField(max_length=1, choices=SETTING_DAYCARE_CHOICES, required=True)
    setting_continuously_open = models.BooleanField(required=True)
    setting_school_relationship = models.BooleanField(required=True)
    setting_establishment_partnership = models.BooleanField(required=True)
    setting_weeks_per_year_open = models.DecimalField(max_digits=3, decimal_places=1, default=38.0, required=True)

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
        (F, 'Weekly Fixed'),
        (U2, 'Under Two Year Old'),
        (2, 'Two Year Old'),
        (O2, 'Over Two Year Old'),
    )
    fees_group = models.CharField(max_length=2, choices=FEE_GROUP)
    fees_hours = models.DecimalField(max_digits=3, decimal_places=2)
    fees_amount = models.DecimalField(max_digits=5, decimal_places=2)

    def __unicode__(self):
        return self.text

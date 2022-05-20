from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class TermsAndConditions(models.Model):
    buyer_terms_and_conditions = RichTextUploadingField(
        help_text= 'Elaborate the Terms and Conditions Buyers are subjects to. Please be clear in your explanation.'
    )
    event_organizer_terms_and_conditions = RichTextUploadingField(
        help_text='Terms and Conditions for Event Owners. This must be clear and straight forward to understand.'
    )
    privacy_policy = RichTextUploadingField(
        help_text= 'Describe how you shall maintain security on the information that users are proving to All1Zed '
                   'Events Platform.', blank=True, null=True
    )
    terms_of_use = RichTextUploadingField(
        help_text='By using All1Zed Events Platform, all stakeholders agree to your specific terms. Describe them here.',
        blank=True, null=True
    )


    def __str__(self):
        return 'Terms And Conditions'

    class Meta:
        verbose_name_plural = 'Terms And Conditions'
        verbose_name = 'Terms And Conditions'



class All1zedBusCommission(models.Model):
    commission_per_ticket = models.FloatField(default=10, help_text='This designates the amount in Zambian Kwacha, that All1Zed gets for each Ticket sold on the platform.')
    def __str__(self):
        return f'K{self.commission_per_ticket} Per Ticket Sold.'

    class Meta:
        verbose_name_plural = ' All1Zed Bus Ticket Commission'
        verbose_name = 'Bus Ticket Commission'

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('cash_in', 'cash_in'), ('payment', 'payment'),
    ]
    TRANSACTION_STATUS = [
        ('successful', 'successful'), ('failed', 'failed'),
    ]
    """
    A Transaction that happens on the system.
    """
    name = models.CharField(max_length=100, blank=True, null=True)
    session_uuid = models.CharField(max_length=255)
    date_time_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=TRANSACTION_STATUS)
    product_id = models.IntegerField()
    amount = models.FloatField()
    phone_number = models.CharField(max_length=15)
    type = models.CharField(choices=TRANSACTION_TYPES, max_length=255)
    request_reference = models.CharField(max_length=255, null=True, blank=True)
    provider_reference = models.CharField(max_length=255)

    def __str__(self):
        return f"Product ID {self.product_id} - {self.status}"

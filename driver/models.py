from django.db import models

# Create your models here.
class Driver_add(models.Model):
    date = models.DateField(null=True, blank=True)
    licen_number =models.CharField(max_length=100, null=False,blank=False)
    driver_name =models.CharField(max_length=100, null=False,blank=False)
    licaen_type =models.CharField(max_length=100, null=False,blank=False)
    mobile_number =models.CharField(max_length=100, null=False,blank=False)
    operator =models.CharField(max_length=100, null=False,blank=False)
    pan_card_pic = models.ImageField(upload_to='driver_pic', null=False, blank=False, default='no_image.png')
    adhar_card = models.ImageField(upload_to='driver_pic', null=False, blank=False, default='no_image.png')

    reference_one = models.CharField(max_length=100, null=False,blank=False)
    reference_two = models.CharField(max_length=100, null=False,blank=False)
    address_one = models.CharField(max_length=100, null=False,blank=False)
    address_two = models.CharField(max_length=100, null=False,blank=False)
    ref_moblie_one = models.CharField(max_length=100, null=True, blank=True)
    ref_moblie_two = models.CharField(max_length=100, null=True, blank=True)

    pair_status = models.BooleanField(default=False)
    pair_with = models.CharField(max_length=100 , null=True)

    def __str__(self):
        return self.licen_number


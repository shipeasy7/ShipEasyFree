from django.db import models

# Create your models here.
class Truck_data(models.Model):

    licanse_number = models.CharField(max_length=100, null=False)
    licanse_image = models.ImageField(upload_to='truck_info', null=False, blank=False , default='no_image.png')
    roc_image = models.ImageField(upload_to='truck_info', null=False, blank=False , default='no_image.png')
    truck_oem = models.CharField(max_length=100, null=False, blank=False)
    model = models.CharField(max_length=100, null=False, blank=False)
    wheels = models.CharField(max_length=100, null=False, blank=False)
    axle_type = models.CharField(max_length=100, null=False, blank=False)

    truck_type = models.CharField(max_length=100, null=False, blank=False)
    truck_capacity = models.CharField(max_length=100, null=False, blank=False)
    truck_lemgth = models.CharField(max_length=100, null=False, blank=False)
    mobile_number = models.CharField(max_length=100, null=False, blank=False)
    operator = models.CharField(max_length=100, null=False, blank=False)

    owener_name = models.CharField(max_length=100, null=False, blank=False)
    conatact = models.CharField(max_length=100, null=False, blank=False)
    pan_card = models.CharField(max_length=100, null=False, blank=False)
    # pan_pic = models.ImageField(upload_to='truck_info', null=False, blank=False, default='no_image.png')
    date_of_fitnace_certificate =  models.DateField(null=True,blank=True)
    pan_card_pic = models.ImageField(upload_to='truck_info', null=False, blank=False, default='no_image.png')
    fitness_certificate = models.ImageField(upload_to='truck_info', null=False, blank=False, default='no_image.png')

    pair_status = models.BooleanField(default=False)
    # pair_with = models.CharField(max_length=100 , null=True)


    def __str__(self):
        return self.licanse_number
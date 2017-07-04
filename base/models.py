from django.db import models
from django.contrib.auth.models import User


# Create your models here.


###### For create New User ######
class Add_user(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.PROTECT, null = True, blank = True,related_name="%(app_label)s_%(class)s_related")
    company_name = models.CharField(max_length=100, null=True, blank= False)
    mobile_number = models.CharField(max_length=100, null= False, blank=False)
    email = models.CharField(max_length=100, null=False, blank=False)
    # password = models.CharField(max_length=100, null=False, blank= False)
    company_logo = models.ImageField(upload_to='profile_pic', default='no_image.png')
    pan_card = models.ImageField(upload_to='profile_pic', default='no_image.png')
    address = models.CharField(max_length=1000, null=True, blank=False)
    landline_number = models.CharField(max_length=100, null = True, blank = False)
    contact_name = models.CharField(max_length=1000, null=True, blank=False)
    designation = models.CharField(max_length=1000, null=True , blank=False)

    def __str__(self):
        return self.user_name

class Password_reset(models.Model):
    emil = models.CharField(max_length=100, null=False, blank=False)
    mobile_number = models.CharField(max_length=100, null=False, blank=False)
    otp = models.CharField(max_length=100, null=False, blank=False)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return self.id

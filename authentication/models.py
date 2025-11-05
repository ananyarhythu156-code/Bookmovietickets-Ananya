from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser

from ticket.models import BaseClass



class RoleChoices(models.TextChoices):

    ADMIN = 'Admin','Admin'
    USER = 'User','User'



class Profile(AbstractUser):
    role = models.CharField(max_length=30,choices=RoleChoices.choices)
    
    phone_num = models.CharField(max_length=15,unique=True)



    class Meta():

          verbose_name = 'Profile'

          verbose_name_plural = 'Profile'


    def _str_(self):
         
         return self.username  
    


class OTP(BaseClass):

     user = models.OneToOneField('Profile',on_delete=models.CASCADE)

     mobile_otp = models.CharField(max_length=4,null=True,blank=True)

     email_otp = models.CharField(max_length=4,null=True,blank=True)

     class Meta():

          verbose_name = 'OTP'

          verbose_name_plural = 'OTP'

     def _str_(self):
         
         return f'{self.user.username}-otp'

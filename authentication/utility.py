import random
import string
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from twilio.rest import Client
from decouple import config



def password_generator():

    password = ''.join(random.choices(string.ascii_letters+string.digits,k=8))


    return password


def Sending_email(subject,template,context,recipient):

    sender = settings.EMAIL_HOST_USER

    email_obj = EmailMultiAlternatives(subject,from_email=sender,to=[recipient])

    content = render_to_string(template,context)

    email_obj.attach_alternative(content,'text/html')

    email_obj.send()   #used to send mail
    
    
    
def Generate_otp():
    
    email_otp = ''.join(random.choices(string.digits,k=4))
    phone_otp = ''.join(random.choices(string.digits,k=4))

    return email_otp,phone_otp



def send_phone_sms(phone_num,otp):
    account_sid = config('ACCOUNT_SID') 
    auth_token = config('AUTH_TOKEN')
    from_num = config('FROM_NUM')
    client = Client(account_sid, auth_token)
    message = client.messages.create(from_=from_num,
                                     body=f'OTP for verification : {otp}',
                                     to='+919496245721'
    )




def send_booking_confirmation(phone_num, movie_name, theater_name, show_time, seats,payment_method):

    account_sid = config('ACCOUNT_SID')

    auth_token = config('AUTH_TOKEN')

    from_num = config('FROM_NUM')

    client = Client(account_sid, auth_token)


    if payment_method == 'Online':

        payment_text = "Payment: ✅ Online Paid"

    else:
        
        payment_text = "Payment: 💵 Pay at Counter"

    msg = (
        f'🎬 Booking Confirmed!\n'
        f'Movie: {movie_name}\n'
        f'Theater: {theater_name}\n'
        f'Show Time: {show_time}\n'
        f'Seats: {seats}\n'
        f'💳 Payment Method: {payment_method}\n'
        f'Enjoy your movie! 🍿'
    )
    
    message = client.messages.create(
        from_=from_num,
        body=msg,
        to='+919496245721'
    )



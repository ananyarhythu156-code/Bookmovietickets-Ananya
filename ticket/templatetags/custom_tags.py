from django import template

register = template.Library()


@register.simple_tag
def get_masked_email_phone(request):

    email = request.user.email

    phone = request.user.phone_num

    username,at,domain = email.partition('@')

    email = '****'+username[5:]+at+domain
    
    phone = '*****'+phone[5:]

    return {'masked_email':email,'masked_phone':phone}
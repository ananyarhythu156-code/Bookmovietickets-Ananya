from django.shortcuts import render,redirect

from django.views import View

from .form import LoginForm,RegisterForm,NewPasswordForm,OTPForm

from django.contrib.auth import login,authenticate,logout

from .utility import password_generator, send_phone_sms,Sending_email,Generate_otp,send_booking_confirmation

from django.contrib.auth.hashers import make_password

from django.db import transaction

import threading

from django.utils.decorators import method_decorator

from authentication.permissions import Permission_roles

from django.utils import timezone

from.models import OTP

from django.contrib import messages

from ticket.models import Movies,Showtime



# Create your views here.



class LoginView(View):

    form_class = LoginForm

    def get(self,request,*args,**kwargs):

        form = self.form_class()

        data = {'form':form}

        return render(request,'authentication/login.html',context=data)
    

    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():

            print(form.cleaned_data)


            user = authenticate(**form.cleaned_data)     # check the user in the db

            if user:

                login(request,user)

                return redirect('home')
            
            msg='Invalid Credential'



        
        data = {'form':form,'msg':msg if 'msg' in locals() else None}

        return render(request,'authentication/login.html',context=data) 



class LogoutView(View):
    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect('home')
    



class RegisterView(View):

    form_class = RegisterForm

    def get(self,request,*args,**kwargs):

        form = self.form_class()

        data = {'form':form}

        return render(request,'authentication/register.html',context=data)  
    



    def post(self,request,*args,**kargs):

        form = self.form_class(request.POST)

        if form.is_valid():

            user = form.save(commit=False)     # save user instance and not save in db

            user.username = user.email

            user.role = 'User'

            password = password_generator()         # custom password ... create random password

            print(password)

            user.password = make_password(password)     #encrypt

            with transaction.atomic():   # save user safely

                user.save()   # only save user


                # sending login credential to email  

            subject = '🎟️ Your Movie Ticket Login Credentials'

            template = 'email/login_credentials.html'

            context = {'user':user,'password':password}

            recipient = user.email

            thread = threading.Thread(target=Sending_email,args=(subject,template,context,recipient))

            thread.start()

            # Sending_email(subject,template,context,recipient)

            return redirect('login')
        
        data = {'form':form}

        return render(request,'authentication/register.html',context= data)



@method_decorator(Permission_roles(['User']),name='dispatch')
class changePasswordView(View):

    form_class = OTPForm

    def get(self,request,*args,**kwargs):

        form = self.form_class()

        email_otp,phone_otp = Generate_otp()   # custum function

        otp,status=OTP.objects.get_or_create(user=request.user)   #udate db as per user 

        otp.email_otp = email_otp

        otp.mobile_otp = phone_otp

        otp.save()

        subject = ' OTP for Change Password'

        template = 'email/email-otp.html'

        context = {'otp':email_otp,'request':request}

        recipient = request.user.email

        thread = threading.Thread(target=Sending_email,args=(subject,template,context,recipient))

        thread.start()

        send_phone_sms(request.user.phone_num,phone_otp)

        request.session['otp_time'] = timezone.now().timestamp()   #generate otp

        remaining_time = 600

       

        data = {'form':form,'remaining_time':remaining_time}

        return render(request,'authentication/otp.html',context=data)
    

    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():

            validate_data = form.cleaned_data
            
            email_otp = validate_data.get('email_otp')

            phone_otp = validate_data.get('phone_otp')

            otp_time = request.session.get('otp_time')

            error = None

            otp = OTP.objects.get(user=request.user)  #take otp from db

            db_email_otp = otp.email_otp

            db_phone_otp = otp.mobile_otp

            if otp_time:

                elapsed = timezone.now().timestamp() - otp_time

                remaining_time = max(0,600-int(elapsed))

                if elapsed - otp_time > 600:

                    error = 'OTP expired request a new one'

                elif email_otp == db_email_otp and phone_otp == db_phone_otp:

                    request.session.pop('otp_time')

                    return redirect('new_password')    # verify otp
                
                else:

                    error = 'invalid OTP'

            

        data = {'form':form,'remaining_time':remaining_time,'error':error}

        return render(request,'authentication/otp.html',context=data)
    
    



@method_decorator(Permission_roles(['User']),name='dispatch')   
class NewPasswordView(View):

    form_class = NewPasswordForm

    def get(self,request,*args,**kwargs):

        form = self.form_class()

        data = {'form':form}

        return render(request,'authentication/new_password.html',context=data)  


    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():

            password = form.cleaned_data.get('password')

            user = request.user

            request.user.password = make_password(password)

            user.save()

            logout(request)

            messages.success(request,'Password sucessfully changed')

            return redirect('login')

        data = {'form':form}

        return render(request,'authentication/new_password.html',context=data)  
    









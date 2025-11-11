from django.shortcuts import render,redirect
from django.utils import timezone
from django.views import View
from .models import Movies,Showtime,Booking,Category,Feedback,Director,Producer,Actor,Actress
from django.utils.decorators import method_decorator
from.form import AddAMovieForm,BookingForm,FeedbackForm
from authentication.permissions import Permission_roles
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.utility import send_booking_confirmation
import threading


from payment.models import Payment

# Create your views here.
class HomeView(View):

    def get(self,request,*args,**kwargs):

        query = request.GET.get('query')    

        now = timezone.now()

        movies = Movies.objects.all()

        coming_soon = movies.filter(category__name='Coming soon')

        now_trending = movies.filter(category__name='Now Trending')

        top_rated = movies.filter(category__name='Top Rated')

        blockbusters = movies.filter(category__name='Blockbusters')

        new_releases = movies.filter(category__name='New Releases')

        if query:

            coming_soon = coming_soon.filter(title__icontains=query)
            now_trending = now_trending.filter(title__icontains=query)
            top_rated = top_rated.filter(title__icontains=query)
            blockbusters = blockbusters.filter(title__icontains=query)
            new_releases = new_releases.filter(title__icontains=query)

           
        data = {
                    'coming_soon': coming_soon,
                    'now_trending': now_trending,
                    'top_rated': top_rated,
                    'blockbusters': blockbusters,
                    'new_releases': new_releases,
                    'page': 'home',
                    'search_query': query,
               }
        return render(request,'tickets/home.html',context=data)
    

class MovieDetailsView(View):

    def get(self, request, *args, **kwargs):

        movie_uuid = request.GET.get('movie')

        movie = Movies.objects.filter(uuid=movie_uuid).first()

        if not movie:

            return redirect('home')
        
        showtimes = Showtime.objects.filter(movie=movie).order_by('theater', 'show_date', 'show_time')
        
    

        data = {
            'movie': movie,
            'showtimes': showtimes,
            'director': movie.director,
            'producer': movie.producer,
            'actor': movie.actor,
            'actress': movie.actress
            
        }
        return render(request, 'tickets/movie_details.html', context=data)




    


class AboutView(View):

    def get(self,request,*args,**kwargs):

        return render(request, 'tickets/about.html')  
      
    

class ContactView(View):

    def get(self,request,*args,**kwargs):
        
        return render(request, 'tickets/contact.html')
    

    def post(self, request, *args, **kwargs):
       
        name = request.POST.get('name')

        email = request.POST.get('email')

        message = request.POST.get('message')

        feedback = Feedback.objects.create(name=name, email=email, message=message)

        return redirect('feedback_page', pk=feedback.pk)

         





@method_decorator(Permission_roles(['Admin']),name='dispatch')
class AddMovieView(View):

    form_class = AddAMovieForm

    def get(self,request,*args,**kwargs):
        
        form = self.form_class()   #create empty form

        data = {'page':'add_movie','form':form}

        return render(request,'tickets/add_movie.html', context=data)
    

    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST,request.FILES)   # pass to object

        if form.is_valid():

            form.save()

            return redirect('home')
        
        
        data = {'page':'add_movie','form':form}
        
        return render(request,'tickets/add_movie.html',context=data)
    

    


@method_decorator(Permission_roles(['User']),name='dispatch')
class BookTicketView(View):

    form_class = BookingForm

    def get(self, request, *args, **kwargs):

        uuid = kwargs.get('uuid')

        movie = Movies.objects.filter(uuid=uuid).first()

        if not movie:
            return redirect('home') 

        # showtime = Showtime.objects.filter(movie=movie)
        showtime_id = request.GET.get('showtime')

        if showtime_id:
            showtime = Showtime.objects.filter(id=showtime_id, movie=movie).first()
        else:
            showtime = Showtime.objects.filter(movie=movie).first()


        form = self.form_class()

        data = {
            'page': 'book_ticket',
            'form': form,
            'movie': movie,
            'showtime': showtime
        }

        return render(request, 'tickets/book_ticket.html',context=data )
    
    
    def post(self, request, *args, **kwargs):

        uuid = kwargs.get('uuid')

        movie = Movies.objects.filter(uuid=uuid).first()

        if not movie:
            
            return redirect('home')  # or render a custom error page

        
        showtime_id = request.GET.get('showtime')

        if showtime_id:

            showtime = Showtime.objects.filter(id=showtime_id, movie=movie).first()
        else:
            showtime = Showtime.objects.filter(movie=movie).first()

        form = self.form_class(request.POST)     # form data assign to the object 

        if form.is_valid():

            booking = form.save(commit=False)

            booking.showtime = showtime

            booking.total_price = booking.seats * movie.price

            payment_method = request.POST.get('payment_method')   #payment handling

            booking.payment_method = payment_method

            if payment_method == 'Online':

                booking.payment_status = 'Paid'  # online → paid automatically after Razorpay success
            else:
                booking.payment_status = 'Not Paid'

            booking.save()
            
            # payment record


            payment_obj = Payment.objects.create(booking=booking,amount=booking.total_price )


            phone_num = request.user.phone_num
            movie_name = movie.title
            theater_name = showtime.theater.name
            show_time = showtime.show_time
            seats = booking.seats
            


            thread = threading.Thread(
                target=send_booking_confirmation,
                args=(phone_num, movie_name, theater_name, show_time, seats, payment_method)
            )
            thread.start()


            # online payment 
            if payment_method == 'Online':

                messages.success(request, '🎟️ Online payment initiated! Confirmation SMS sent.')
                
                return redirect('razorpay', uuid=payment_obj.uuid)
            
            else:
                booking.is_confirmed = True    #offline

                booking.save()

                messages.success(request, '🎟️ Ticket booked successfully! (Cash Payment)')
               
                return redirect('booking_confirmation', uuid=booking.uuid)


        return render(request, 'tickets/book_ticket.html', {
            'page': 'book_ticket',
            'form': form,
            'movie': movie,
            'showtime': showtime
        })


@method_decorator(Permission_roles(['User']),name='dispatch')
class BookingConfirmationView(View):

    def get(self, request, *args, **kwargs):

        booking_uuid = kwargs.get('uuid')

        booking = Booking.objects.filter(uuid=booking_uuid).first()

        if not booking:


            return redirect('home')  # or render a custom error page
        

        if request.user.is_authenticated and request.user.phone_num:

            movie_name = booking.showtime.movie.title

            theater_name = booking.showtime.theater.name

            show_time = f"{booking.showtime.show_date} {booking.showtime.show_time}"

            seats = booking.seats

            phone_num = request.user.phone_num

            payment_method = booking.payment_method


            thread = threading.Thread(
                target=send_booking_confirmation,
                args=(phone_num, movie_name, theater_name, show_time, seats,payment_method)
            )
            thread.start()


            messages.success(request, "🎬 Booking confirmation SMS sent successfully!")
 
           

        return render(request, 'tickets/booking_confirmation.html', {
            'booking': booking
        })




@method_decorator(Permission_roles(['User']),name='dispatch')
class MyBookingsView(View):

    def get(self, request, *args, **kwargs):
        
        bookings = Booking.objects.all().order_by('-created_at')

        data = {
            'page': 'my_bookings',
            'bookings': bookings
        }

        return render(request, 'tickets/mybookings.html', context=data)
    




class AddFeedbackView(View):

    def get(self, request, *args, **kwargs):

        return render(request, 'tickets/add_feedback.html')

    def post(self, request, *args, **kwargs):

        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Feedback.objects.create(
            name=name,
            email=email,
            message=message
        )
        return redirect('home')
    

@method_decorator(Permission_roles(['Admin']),name='dispatch')
class FeedbackView(View):

    def get(self, request, *args, **kwargs):

        feedbacks = Feedback.objects.all().order_by('-created_at')
        
        return render(request, 'tickets/feedback.html', {'feedbacks': feedbacks})   




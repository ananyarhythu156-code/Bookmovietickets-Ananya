from django.urls import path

from . import views

urlpatterns =[
            path('',views.HomeView.as_view(),name='home'),
            path('movie_details/',views.MovieDetailsView.as_view(),name='movie_details'),
            path('about/',views.AboutView.as_view(),name='about'),
            path('contact/',views.ContactView.as_view(),name='contact'),
            path('add_movie/',views.AddMovieView.as_view(),name='add_movie'),
            path('book/<uuid:uuid>/',views.BookTicketView.as_view(),name='book'),
            path('booking_confirmation/<uuid:uuid>/', views.BookingConfirmationView.as_view(), name='booking_confirmation'),
            path('mybookings/',views.MyBookingsView.as_view(),name='mybookings'),
            path('feedback/', views.FeedbackView.as_view(), name='feedback'),
            path('add-feedback/', views.AddFeedbackView.as_view(), name='add_feedback'),
            
             


]
from django.db import models
from django.conf import settings

# Create your models here.

import uuid 

class BaseClass(models.Model):

    uuid = models.UUIDField(default= uuid.uuid4,unique=True)

    active_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)


    class Meta:

        abstract = True




class Category(BaseClass):

    name = models.CharField(max_length=50)

    class Meta:
        

        verbose_name = 'Categories'

        verbose_name_plural = 'Categories'


    def __str__(self):
        return f'{self.name}' 


class Genre(BaseClass):

     name = models.CharField(max_length=50)

     class Meta:
        

        verbose_name = 'Genre'

        verbose_name_plural = 'Genre'



     def __str__(self):
            
            return f'{self.name}'  
     

class Director(BaseClass):


    name = models.CharField(max_length=100)

    image = models.ImageField(upload_to='directors/', null=True, blank=True)

    

    

    class Meta:
        

        verbose_name = 'Director'

        verbose_name_plural = 'Director'



    def __str__(self):
            
            return f'{self.name}'    
    

class Producer(BaseClass):

    name = models.CharField(max_length=100)

    image = models.ImageField(upload_to='cast/', null=True, blank=True)

    

    class Meta:

        verbose_name = 'Producer'

        verbose_name_plural = 'Producer'

    def __str__(self):

        return self.name


class Actor(BaseClass):

    name = models.CharField(max_length=100)

    image = models.ImageField(upload_to='cast/', null=True, blank=True)

    

    class Meta:

        verbose_name = 'Actor'

        verbose_name_plural = 'Actor'

    def __str__(self):

        return self.name


class Actress(BaseClass):

    name = models.CharField(max_length=100)

    image = models.ImageField(upload_to='cast/', null=True, blank=True)

    

    class Meta:

        verbose_name = 'Actress'

        verbose_name_plural = 'Actress'

    def __str__(self):

        return self.name





class Movies(BaseClass):

    title = models.CharField(max_length=100)

    description = models.TextField()

    poster = models.ImageField(upload_to= 'movies/')

    category =  models.ForeignKey('Category',on_delete = models.CASCADE)

    genre = models.ForeignKey('Genre',on_delete = models.CASCADE )
    
    director = models.ForeignKey('Director', on_delete=models.SET_NULL, null=True, blank=True, related_name='movies')

    producer = models.ForeignKey(Producer, on_delete=models.SET_NULL, null=True, blank=True)

    actor = models.ForeignKey(Actor, on_delete=models.SET_NULL, null=True, blank=True)

    actress = models.ForeignKey(Actress, on_delete=models.SET_NULL, null=True, blank=True)

    duration = models.CharField(max_length=20)  # e.g., "2h 14m"

    release_year = models.IntegerField()

    is_available = models.BooleanField(default=True)

    price = models.FloatField(default=0.0)



    class Meta:
        
       

        verbose_name = 'movies'

        verbose_name_plural = 'movies'


    def __str__(self):
        return f'{self.title}-{self.category.name}' 



class Theater(BaseClass):

    name = models.CharField(max_length=200)

    # location = models.CharField(max_length=150)

    # latitude = models.FloatField(blank=True, null=True)

    # longitude = models.FloatField(blank=True, null=True)

    total_seats = models.IntegerField()

    class Meta:
        
       

        verbose_name = 'theater'

        verbose_name_plural = 'theater'


    def __str__(self):

        return self.name




class Showtime(BaseClass):

    movie = models.ForeignKey('Movies', on_delete=models.CASCADE, related_name='showtimes')
    theater = models.ForeignKey('Theater', on_delete=models.CASCADE)
    show_date = models.DateField(null=True, blank=True)  
    show_time = models.TimeField(null=True, blank=True)
    class Meta:
        
        verbose_name = 'Showtime'

        verbose_name_plural = 'Showtime'


    def __str__(self):

        return f"{self.movie.title} at {self.theater.name} on {self.show_time}"



class Booking(BaseClass):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    seats = models.PositiveIntegerField()
    total_price = models.FloatField(default=0.0)
    payment_method = models.CharField( max_length=20, choices=[('Online', 'Online Payment'),('Offline', 'Pay at Counter') ],default='Online')
    payment_status = models.CharField(max_length=20,choices=[('Paid', 'Paid'),('Not Paid', 'Not Paid')],default='Not Paid')
    



    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.showtime.movie.title}"
        return f"{self.name} - {self.showtime.movie.title}"              # # safely handle both user or guest
    



class Feedback(BaseClass):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}" 
    








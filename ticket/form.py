from django import forms
from .models import Movies,Genre,Category,Booking,Feedback

class AddAMovieForm(forms.ModelForm):

    pass
   
    class Meta: 

        model = Movies

        exclude = ['uuid','active_status']


        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter movie title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter movie description'}),
            'poster': forms.FileInput(attrs={'class':'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2h 14m'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2025'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 250'}),
            'is_available' : forms.RadioSelect(choices=[(True,'Yes'),(False,'No')],attrs={'class' : 'form-check-input'})
        }
         


    category = forms.ModelChoiceField(queryset=Category.objects.all(),widget=forms.Select(attrs={'class':'form-select','required':'required'}))


    genre = forms.ModelChoiceField(queryset=Genre.objects.all(),widget=forms.Select(attrs={'class': 'form-select', 'required': 'required'}))


    def __init__(self,*args,**kwargs):

        super(AddAMovieForm,self).__init__(*args,**kwargs)

        if not self.instance:
            self.fields.get('poster').widget.attrs['required'] = 'required'





# 🎟️ Ticket / Booking Form
class BookingForm(forms.ModelForm):

    class Meta:

        model = Booking
        
        fields = ['name', 'seats']

        labels = {
            'name': 'Your Name',
            'seats': 'Number of Seats',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'seats': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'No. of seats'}),

        }




class FeedbackForm(forms.ModelForm):

    class Meta:

        model = Feedback

        fields = ['name', 'email', 'message']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border-warning shadow-sm','placeholder': 'Enter your name' }),

            'email': forms.EmailInput(attrs={'class': 'form-control border-warning shadow-sm','placeholder': 'Enter your email'}),

            'message': forms.Textarea(attrs={'class': 'form-control border-warning shadow-sm','placeholder': 'Write your feedback...','rows': 4 }),
        }

    def __init__(self, *args, **kwargs):

        super(FeedbackForm, self).__init__(*args, **kwargs)

        # Add a consistent Bootstrap look for all fields
        for field in self.fields.values():

            existing_classes = field.widget.attrs.get('class', '')
            
            field.widget.attrs['class'] = f'{existing_classes} bg-dark text-light'        
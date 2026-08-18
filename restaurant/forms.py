from django.forms import ModelForm, DateInput
from .models import Booking


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['first_name', 'reservation_date', 'reservation_slot']
        widgets = {
            'reservation_date': DateInput(attrs={'type': 'date'}),
        }

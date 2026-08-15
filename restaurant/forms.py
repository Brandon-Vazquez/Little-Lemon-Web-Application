from django import forms
from django.forms import ModelForm, DateInput
from .models import Booking


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ['first_name', 'reservation_date', 'reservation_slot']
        widgets = {
            'reservation_date': DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        reservation_date = cleaned_data.get('reservation_date')
        reservation_slot = cleaned_data.get('reservation_slot')

        if reservation_date and reservation_slot is not None:
            if Booking.objects.filter(
                reservation_date=reservation_date,
                reservation_slot=reservation_slot,
            ).exists():
                raise forms.ValidationError(
                    'This time slot is already booked for the selected date.'
                )

        return cleaned_data

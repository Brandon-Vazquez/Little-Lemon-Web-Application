from rest_framework import serializers

from .models import Booking, Menu


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'name', 'price', 'menu_item_description']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'first_name', 'reservation_date', 'reservation_slot', 'user']
        read_only_fields = ['user']

    def validate(self, data):
        reservation_date = data.get('reservation_date', getattr(self.instance, 'reservation_date', None))
        reservation_slot = data.get('reservation_slot', getattr(self.instance, 'reservation_slot', None))

        qs = Booking.objects.filter(
            reservation_date=reservation_date,
            reservation_slot=reservation_slot,
        )
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                'This time slot is already booked for the selected date.'
            )
        return data

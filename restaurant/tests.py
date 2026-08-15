from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Booking, Menu


class MenuModelTest(APITestCase):
    def test_menu_str(self):
        item = Menu.objects.create(name='Greek Salad', price=12, menu_item_description='Fresh salad')
        self.assertEqual(str(item), 'Greek Salad')


class MenuApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='testpass123')
        self.menu_item = Menu.objects.create(name='Bruschetta', price=8, menu_item_description='Toasted bread')

    def test_list_menu_items_unauthenticated(self):
        response = self.client.get(reverse('menu-items'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_menu_item_requires_authentication(self):
        response = self.client.post(reverse('menu-items'), {
            'name': 'Pasta',
            'price': 15,
            'menu_item_description': 'Homemade pasta',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_menu_item_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('menu-items'), {
            'name': 'Pasta',
            'price': 15,
            'menu_item_description': 'Homemade pasta',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 2)


class BookingApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='testpass123')

    def test_list_bookings_requires_authentication(self):
        response = self.client.get(reverse('booking-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_booking_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('booking-list'), {
            'first_name': 'Mario',
            'reservation_date': '2026-08-20',
            'reservation_slot': 12,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Booking.objects.first().user, self.user)

    def test_create_booking_duplicate_slot_rejected(self):
        self.client.force_authenticate(user=self.user)
        Booking.objects.create(user=self.user, first_name='Mario', reservation_date='2026-08-20', reservation_slot=12)
        response = self.client.post(reverse('booking-list'), {
            'first_name': 'Adrian',
            'reservation_date': '2026-08-20',
            'reservation_slot': 12,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_bookings_by_date(self):
        self.client.force_authenticate(user=self.user)
        Booking.objects.create(user=self.user, first_name='Mario', reservation_date='2026-08-20', reservation_slot=12)
        Booking.objects.create(user=self.user, first_name='Adrian', reservation_date='2026-08-21', reservation_slot=13)
        response = self.client.get(reverse('booking-list'), {'date': '2026-08-20'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'Mario')

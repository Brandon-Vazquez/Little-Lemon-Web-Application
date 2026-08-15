# from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse

from .models import Menu
from django.core import serializers
from .models import Booking
from datetime import datetime
import json
from .forms import BookingForm

from rest_framework import generics, permissions

from .serializers import BookingSerializer, MenuSerializer


class MenuItemsView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookingListView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Booking.objects.all()
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(reservation_date=date)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookingView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            form = BookingForm()
    context = {'form': form}
    return render(request, 'book.html', context)

def bookings(request):
    date = request.GET.get('date', datetime.today().date())
    bookings = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)
    return JsonResponse(booking_json, safe=False)



def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 
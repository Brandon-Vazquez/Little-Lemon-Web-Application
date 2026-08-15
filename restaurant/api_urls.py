from django.urls import path

from . import views

urlpatterns = [
    path('menu/', views.MenuItemsView.as_view(), name='menu-items'),
    path('menu/<int:pk>/', views.MenuItemView.as_view(), name='menu-item'),
    path('bookings/', views.BookingListView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', views.BookingView.as_view(), name='booking-detail'),
]

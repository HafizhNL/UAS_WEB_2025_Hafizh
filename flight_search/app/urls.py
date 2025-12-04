from django.urls import path
from . import views

urlpatterns = [
    # === HTML Pages ===
    path('', views.search_flight_page, name='search_flight'),
    path('results/', views.flight_results_page, name='flight_results'),
    path('booking/', views.flight_booking_page, name='flight_booking'),
    path('booking/confirmation/<str:booking_id>/', views.booking_confirmation_page, name='booking_confirmation'),
    
    # API Endpoints
    path('api/search-flights/', views.SearchFlightsAPIView.as_view(), name='api_search_flights'),
    path('api/confirm-booking/', views.CreateBookingAPIView.as_view(), name='api_confirm_booking'),

    
]
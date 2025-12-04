from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .service import AmadeusService
from .models import Booking
from .serializer import FlightSearchSerializer, BookingCreateSerializer, BookingSerializer
import random
import string

# Frontend Pages

def search_flight_page(request):
    return render(request, 'search_flight.html')

def flight_results_page(request):
    return render(request, 'flight_results.html')

def flight_booking_page(request):
    return render(request, 'flight_booking.html')

def booking_confirmation_page(request, booking_id=None):
    return render(request, 'booking_confirmation.html', {
        'booking_id': booking_id
    })

# Helper Functions

def extract_flight_data(flight_offer):
    """Extract flight data dari Amadeus response"""
    try:
        flight_id = flight_offer.get('id', '')
        
        price_data = flight_offer.get('price', {})
        currency = price_data.get('currency', 'IDR')
        total = price_data.get('total', '0')
        price = f"{currency} {total}"
        
        itineraries = flight_offer.get('itineraries', [])
        if itineraries:
            segments = itineraries[0].get('segments', [])
            if segments:
                first_seg = segments[0]
                last_seg = segments[-1]
                
                carrier = first_seg.get('carrierCode', '')
                number = first_seg.get('number', '')
                origin = first_seg.get('departure', {}).get('iataCode', '')
                destination = last_seg.get('arrival', {}).get('iataCode', '')
                dep_time = first_seg.get('departure', {}).get('at', '')[:16]
                arr_time = last_seg.get('arrival', {}).get('at', '')[:16]
                
                flight_info = f"{carrier}{number} {origin} → {destination}, {dep_time} - {arr_time}"
            else:
                flight_info = "Flight information not available"
        else:
            flight_info = "Flight information not available"
        
        return {
            'flight_id': flight_id,
            'flight_info': flight_info,
            'price': price  
        }
        
    except Exception as e:
        return {
            'flight_id': flight_offer.get('id', 'unknown'),
            'flight_info': 'Error extracting flight info',
            'price': 'N/A'
        }


# API

class SearchFlightsAPIView(APIView):
    """Search flights dari Amadeus"""
    serializer_class = FlightSearchSerializer
    
    def post(self, request):
        serializer = FlightSearchSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        origin = validated_data['origin']
        destination = validated_data['destination']
        departure_date = validated_data['departure_date'].strftime('%Y-%m-%d')
        return_date = validated_data.get('return_date')
        if return_date:
            return_date = return_date.strftime('%Y-%m-%d')
        adults = validated_data.get('adults', 1)
        
        try:
            amadeus_service = AmadeusService()
            flights = amadeus_service.search_flights(
                origin=origin,
                destination=destination,
                departure_date=departure_date,
                return_date=return_date,
                adults=adults
            )
            
            if not flights:
                return Response({
                    'success': False,
                    'message': 'No flights found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Format flights
            formatted_flights = []
            for flight in flights:
                extracted = extract_flight_data(flight)
                formatted_flights.append({
                    'flight_id': extracted['flight_id'],
                    'flight_info': extracted['flight_info'],
                    'price': extracted['price']  # Hanya untuk display
                })
            
            return Response({
                'success': True,
                'count': len(formatted_flights),
                'data': formatted_flights
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateBookingAPIView(APIView):
    """Create booking - sesuai wireframe"""
    serializer_class = BookingCreateSerializer
    
    def post(self, request):
        serializer = BookingCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        
        # Generate booking reference
        booking_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        try:
            # Simpan ke database (tanpa price)
            booking = Booking.objects.create(
                flight_id=validated_data['flight_id'],
                flight_info=validated_data['flight_info'],
                passenger_name=validated_data['passenger_name'],
                passport_number=validated_data['passport_number'],
                booking_reference=booking_ref
            )
            
            return Response({
                'success': True,
                'message': 'Booking confirmed!',
                'data': BookingSerializer(booking).data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BookingListAPIView(generics.ListAPIView):
    """List semua bookings"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'success': True,
            'count': queryset.count(),
            'data': serializer.data
        })


class BookingDetailAPIView(generics.RetrieveAPIView):
    """Get booking by ID"""
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'id'
from rest_framework import serializers
from .models import Booking

class FlightSearchSerializer(serializers.Serializer):
    """Serializer untuk search flight"""
    origin = serializers.CharField(max_length=3, required=True)
    destination = serializers.CharField(max_length=3, required=True)
    departure_date = serializers.DateField(required=True)
    return_date = serializers.DateField(required=False, allow_null=True)
    adults = serializers.IntegerField(default=1, min_value=1, max_value=9)
    
    def validate_origin(self, value):
        if len(value) != 3:
            raise serializers.ValidationError("Airport code must be 3 letters")
        return value.upper()
    
    def validate_destination(self, value):
        if len(value) != 3:
            raise serializers.ValidationError("Airport code must be 3 letters")
        return value.upper()


class BookingCreateSerializer(serializers.Serializer):
    """
    Serializer untuk create booking
    Sesuai wireframe: hanya flight_info, name, passport
    """
    flight_id = serializers.CharField(
        max_length=255,
        required=True,
        help_text="Flight offer ID from Amadeus API"
    )
    
    flight_info = serializers.CharField(
        required=True,
        help_text="Formatted flight information"
    )
    
    passenger_name = serializers.CharField(
        max_length=255,
        required=True,
        help_text="Passenger full name"
    )
    
    passport_number = serializers.CharField(
        max_length=50,
        required=True,
        help_text="Passport number"
    )


class BookingSerializer(serializers.ModelSerializer):
    """Serializer untuk display booking"""
    class Meta:
        model = Booking
        fields = '__all__'
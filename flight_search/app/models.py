from django.db import models

class Booking(models.Model):
    flight_id = models.CharField(max_length=255)
    flight_info = models.TextField()
    passenger_name = models.CharField(max_length=255)
    passport_number = models.CharField(max_length=50)
    booking_reference = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.booking_reference} - {self.passenger_name}"


    


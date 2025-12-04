from amadeus import Client, ResponseError
from django.conf import settings

class AmadeusService:
    def __init__(self):
        self.amadeus = Client(
            client_id=settings.AMADEUS_API_KEY,
            client_secret=settings.AMADEUS_API_SECRET,
            hostname=settings.AMADEUS_HOSTNAME
        )
    
    def search_flights(self, origin, destination, departure_date, return_date=None, adults=1):
        """
        Search for flights
        """
        try:
            params = {
                'originLocationCode': origin,
                'destinationLocationCode': destination,
                'departureDate': departure_date,
                'adults': adults,
                'max': 10,
                'currencyCode': 'IDR'
            }
            
            if return_date:
                params['returnDate'] = return_date
            
            response = self.amadeus.shopping.flight_offers_search.get(**params)
            return response.data
        
        except ResponseError as error:
            print(f"Amadeus API Error: {error}")
            return None
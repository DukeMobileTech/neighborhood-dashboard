from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from geopy.exc import GeocoderServiceError

def reverse_geocode(lat, lon):
    geolocator = Nominatim()
    try:
        location = geolocator.reverse("{}, {}".format(lat, lon), timeout=30)
        return location
    except GeocoderTimedOut as e:
        print 'Error: reverse geocode failed on input with exception GeocoderTimedOut'
        return None
    except GeocoderServiceError as e:
        print 'Error: reverse geocode failed on input with exception GeocoderServiceError'
        return None

if __name__ == "__main__":
    result = reverse_geocode('51.55447', '0.8025423')
    print result.raw['address']['country_code']

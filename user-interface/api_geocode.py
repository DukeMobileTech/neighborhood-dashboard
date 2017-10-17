from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut
from geopy.exc import GeocoderServiceError


def reverse_geocode(lat, lon):
    geolocator = Nominatim()
    try:
        location = geolocator.reverse("{}, {}".format(lat, lon), timeout=30)
        return location
    except GeocoderTimedOut as e:
        print 'Reverse geocode failed with exception GeocoderTimedOut'
        return None
    except GeocoderServiceError as e:
        print 'Reverse geocode failed with exception GeocoderServiceError'
        return None


def google_reverse_geocode(lat, lon, key):
    geolocator = GoogleV3(api_key=key)
    try:
        locations = geolocator.reverse("{}, {}".format(lat, lon), timeout=30)
        return locations
    except GeocoderTimedOut as e:
        print 'Reverse geocoder failed with GeocoderTimedOut'
        return None
    except GeocoderServiceError as e:
        print 'Reverse geocoder failed with GeocoderServiceError'
        return None


if __name__ == "__main__":
    result = reverse_geocode('51.55447', '0.8025423')
    print result.raw['address']['country_code']

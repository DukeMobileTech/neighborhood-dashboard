import api_geocode
import requests
import xml.etree.ElementTree as ET

from common import *

ZILLOW_DEEP_SEARCH_BASE_URL = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm'
locations = []


def getLocationAddress(lat, lon, key):
    locations = api_geocode.google_reverse_geocode(lat, lon, key)
    if locations is not None:
        return locations[0]


def getLocationZestimate(location, api_key):
    # Address from Nominatim
    # address_components = address.split(',')
    # zip_code = address_components[len(address_components) - 2].strip()
    # street = address
    # if address_components[0].strip().isdigit():
    #     print '0 isdigit'
    #     street = address_components[0].strip() + ' ' + address_components[1].strip()
    # elif address_components[1].strip().isdigit():
    #     print '1 isdigit'
    #     street = address_components[1].strip() + ' ' + address_components[2].strip()
    # print 'street is ' + street

    # Address from GoogleV3
    if location is None:
        return
    print location.address
    address_components = location.address.split(',')
    zip_components = address_components[len(
        address_components) - 2].strip().split()
    zip_code = zip_components[1]
    street_1 = address_components[0]
    street_2 = None
    street_components = address_components[0].split(' ')
    if '-' in street_components[0]:
        one, two = street_components[0].split('-')
        street_1 = one + ' ' + ' '.join(street_components[1:])
        street_2 = two + ' ' + ' '.join(street_components[1:])
    params = {
        'zws-id': api_key,
        'address': street_1,
        'citystatezip': zip_code,
        'rentzestimate': True
    }
    try:
        r = requests.get(ZILLOW_DEEP_SEARCH_BASE_URL, params=params)
        # Tree has 3 nodes: request, message, response
        response = ET.fromstring(r.text).findall('response')
        if len(response) == 0 and street_2 is not None:
            r = requests.get(ZILLOW_DEEP_SEARCH_BASE_URL, params={
                             'zws-id': api_key, 'address': street_2, 'citystatezip': zip_code, 'rentzestimate': True})
            # Tree has 3 nodes: request, message, response
            response = ET.fromstring(r.text).findall('response')
        return response
    except Exception as e:
        print 'Exception Raised'
        print e
    except ET.ParseError:
        print 'XML Error'


def parseZestimates(response, family_id, geocode_address, latitude, longitude):
    if response is not None and len(response) > 0:
        results = response[0].findall('results')[0].find('result')
        zestimate = results.find('zestimate')
        rentzestimate = results.find('rentzestimate')
        address = results.find('address')
        street_address = address.find('street').text + ' ' + address.find(
            'city').text + ' ' + address.find('state').text + ' ' + address.find('zipcode').text

        row = {
            'family_id': family_id,
            'latitude': latitude,
            'longitude': longitude,
            'reverse_geocode_address': geocode_address,
            'zpid': results.find('zpid').text,
            'zestimate_amount': zestimate.find('amount').text,
            'zestimate_amount_low': zestimate.find('valuationRange').find('low').text,
            'zestimate_amount_high': zestimate.find('valuationRange').find('high').text,
            'zestimate_date': zestimate.find('last-updated').text,
            'rentzestimate_amount': rentzestimate.find('amount').text,
            'rentzestimate_date': rentzestimate.find('last-updated').text,
            'rentzestimate_amount_low': rentzestimate.find('valuationRange').find('low').text,
            'rentzestimate_amount_high': rentzestimate.find('valuationRange').find('high').text,
            'neighbourhood': results.find('localRealEstate').find('region').get('name') if (results.find('localRealEstate') is not None and results.find('localRealEstate').find('region') is not None) is True else None,
            'use_code': results.find('useCode').text if results.find('useCode') is not None else None,
            'tax_assessment_year': results.find('taxAssessmentYear').text if results.find('taxAssessmentYear') is not None else None,
            'tax_assessment': results.find('taxAssessment').text if results.find('taxAssessment') is not None else None,
            'year_built': results.find('yearBuilt').text if results.find('yearBuilt') is not None else None,
            'lot_size': results.find('lotSizeSqFt').text if results.find('lotSizeSqFt') is not None else None,
            'finished_size': results.find('finishedSqFt').text if results.find('finishedSqFt') is not None else None,
            'bathrooms': results.find('bathrooms').text if results.find('bathrooms') is not None else None,
            'bedrooms': results.find('bedrooms').text if results.find('bedrooms') is not None else None,
            'total_rooms': results.find('totalRooms').text if results.find('totalRooms') is not None else None,
            'last_sold_date': results.find('lastSoldDate').text if results.find('lastSoldDate') is not None else None,
            'last_sold_price': results.find('lastSoldPrice').text if results.find('lastSoldPrice') is not None else None,
            'zillow_address': street_address,
            'zillow_latitude': address.find('latitude').text,
            'zillow_longitude': address.find('longitude').text
        }
        print row
    else:
        row = {'family_id': family_id,
               'latitude': latitude,
               'longitude': longitude,
               'reverse_geocode_address': geocode_address}
    return row


def writeZestimateHeadersToCsv(csvfolder, filename):
    if not os.path.exists(csvfolder):
        os.makedirs(csvfolder)
    initCSV(os.path.join(csvfolder, filename), CSV_ZILLOW_FIELDNAMES)


def writeZestimateDictionaryToCsv(data, csvfolder, filename):
    if not os.path.exists(csvfolder):
        os.makedirs(csvfolder)
    appendCSV(data, os.path.join(csvfolder, filename), CSV_ZILLOW_FIELDNAMES)


def getZestimate(family_id, lat, lon, zillow_key, gsv_key):
    address = getLocationAddress(lat, lon, gsv_key)
    result = getLocationZestimate(address, zillow_key)
    return parseZestimates(result, family_id, address, lat, lon)

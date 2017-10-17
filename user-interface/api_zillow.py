import api_geocode
import requests
import xml.etree.ElementTree as ET
import sys
import getopt
import ConfigParser
import datetime
import os
import json
import osmroad
from distutils.dir_util import copy_tree
from common import *
import familydata


ZILLOW_DEEP_SEARCH_BASE_URL = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm'
locations = []


def getLocationAddress(lat, lon, key):
    locations = api_geocode.google_reverse_geocode(lat, lon, key)
    if locations is not None:
        return locations[0]


def getLocationZestimate(location, api_key):
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


class Zestimator:
    def __init__(self, config_file):
        print '__init__'
        self.config = ConfigParser.RawConfigParser(allow_no_value=True)
        self.config.read(config_file)
        self.gsv_api_key = self.get_secure_config('api-keys', 'gsv', DEFAULT_GSV_KEY)
        self.zillow_key = self.get_secure_config('api-keys', 'zillow', None)
        self.perform_zestimate = self.zillow_key is not None and not (self.zillow_key == 'None')


    def get_secure_config(self, section, option, default):
        if not self.config.has_option(section, option):
            return default
        return self.config.get(section, option)


    def create_directories(self):
        from_directory = HTML_SOURCE_FOLDER
        self.output_directory = self.get_secure_config('settings', 'output-directory', DEFAULT_OUTPUT_FOLDER)
        copy_tree(from_directory, self.output_directory)
        self.csvfolder = os.path.join(self.output_directory, CSV_PATH)


    def load_input_files(self):
        # Location file loading
        if not self.config.has_option('files', 'location'):
            raise Exception('Location file not configured. Check your config file!')
        location_file = self.config.get('files', 'location')
        if not os.path.isfile(location_file):
            raise Exception('Location file not found. Check if the file exists and check your config file!')
        self.location_data = familydata.readCoordinates(location_file)

    def zestimateWithFake(self, family, lat, lon, random_locations):
        random.seed()
        family_done = False
        active = True
        while active:
            rnd = random.randint(0, self.fake_count)
            if rnd > 0 and len(random_locations) > 0:
                fake_location = random_locations.pop(random.randint(0, len(random_locations) - 1))
                print 'Fake request %s' % (fake_location)
                getLocationZestimate(getLocationAddress(lat, lon, self.gsv_api_key), self.zillow_key)
            elif not family_done:
                print 'Real request %s, %s' % (lat, lon)
                zestimate_data = getZestimate(family, lat, lon, self.zillow_key, self.gsv_api_key)
                writeZestimateDictionaryToCsv(zestimate_data, self.csvfolder, 'zestimate_data.csv')
                family_done = True
            if family_done and len(random_locations) == 0:
                active = False


    def process(self):
        print 'Process Launched'
        if self.perform_zestimate:
            print 'Processing zestimates'
            self.create_directories()
            self.load_input_files()
            writeZestimateHeadersToCsv(self.csvfolder, 'zestimate_data.csv')
            self.fake_count = 0
            if self.get_secure_config('settings', 'fake-requests', DEFAULT_FAKE_REQUESTS) == '1':
                self.fake_count = int(self.get_secure_config('settings', 'fake-requests-count', DEFAULT_FAKE_REQUESTS_COUNT))
            counter = 0
            for family in self.location_data:
                counter += 1
                printHeadline(
                    '%s Processing family %s %s/%s' % (datetime.datetime.now(), family, counter, len(self.location_data)))
                if not 'latitude' in self.location_data[family] or not 'longitude' in self.location_data[family] or not \
                        self.location_data[family]['latitude'] or not self.location_data[family]['longitude']:
                    print 'Family %s does not have a location' % (family)
                    continue
                try:
                    lat = float(self.location_data[family]['latitude'])
                    lon = float(self.location_data[family]['longitude'])
                except:
                    print 'Could not convert coordinates to float for family %s' % (family)
                    continue

                if self.fake_count == 0:
                    print 'No fake requests'
                    zestimate_data = getZestimate(family, lat, lon, self.zillow_key, self.gsv_api_key)
                    writeZestimateDictionaryToCsv(zestimate_data, self.csvfolder, 'zestimate_data.csv')
                else:
                    print 'Include fake requests'
                    random_locations = getRandomLocations(lat, lon, self.fake_count)
                    print random_locations
                    self.zestimateWithFake(family, lat, lon, random_locations)
        else:
            print 'Zestimates not performed'


if __name__ == "__main__":
    config_file = 'config.cfg'
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hc:",["cfile="])
        for opt, arg in opts:
            if opt == '-h':
                print '-h'
                sys.exit(0)
            elif opt in ("-c", "--cfile"):
                config_file = arg
    except getopt.GetoptError:
        print 'Error: '
        sys.exit(2)
    zillow = Zestimator(config_file)
    zillow.process()

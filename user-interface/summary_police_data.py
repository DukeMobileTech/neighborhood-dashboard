import os
import csv
import urllib2
import json

data_folder = '../neighbourhood'

def parseNeighbourhoodData():
    neighbourhood_data = []
    for monthly_data_folder in os.listdir(data_folder):
        # print monthly_data_folder
        monthly_data_path = os.path.join(data_folder, monthly_data_folder)
        if os.path.isdir(monthly_data_path):
            # print 'is dir'
            year_and_month = monthly_data_folder.split('-')
            if len(year_and_month) == 2:
                year = year_and_month[0]
                month = year_and_month[1]
                # print year
                # print month
            # print monthly_data_folder
            for neighborhood_file in os.listdir(monthly_data_path):
                # print neighborhood_file
                # neighbourhood_name = neighborhood_file[8:].split('-neighbourhood.csv')[0]
                # print neighbourhood_name
                # actual_neighbourhood_name = ' '.join(neighbourhood_name.split('-'))
                # print actual_neighbourhood_name
                csv_file_path = os.path.join(monthly_data_path, neighborhood_file)
                with open(csv_file_path, 'rb') as csvfile:
                    csv_reader = csv.DictReader(csvfile)
                    for row in csv_reader:
                        # print ', '.join(row)
                        # print row
                        month = row['Month'].split('-')
                        # row['Month'] = month[1]
                        row['Year'] = month[0]
                        # row['NeighbourhoodName'] = actual_neighbourhood_name.title()
                        # print row
                        neighbourhood_data.append(row)
    return neighbourhood_data

def getNeighbourhood(lat, lon):
    print 'Getting neighbourhood for lat ' + str(lat) + ' and lon ' + str(lon)
    uri = 'https://data.police.uk/api/locate-neighbourhood?q=' + str(lat) + ',' + str(lon)
    print uri
    neighbourhood = {}
    try:
        resource = urllib2.urlopen(uri)
        if resource is not None:
            neighbourhood = json.load(resource)
    except urllib2.HTTPError as e:
        print 'The server could not fulfill the request. Error code: ', e.code
    except urllib2.URLError as e:
        print 'The server could not be reached. Reason: ', e.reason
    except:
        print 'An uknown exception was thrown.'
    return neighbourhood

def getNeighbourhoodCrime(family_id, lat, lon, years, summary_data):
    neighbourhood = getNeighbourhood(lat, lon)
    print 'Getting neighbourhood crime for ' + neighbourhood['neighbourhood']
    time_range = years.split('-')
    neighbourhood_summary = []
    for summary_item in summary_data:
        if summary_item['Neighbourhood'] == neighbourhood['neighbourhood'] and summary_item['Year'] in time_range:
            print 'Found'
            neighbourhood_summary.append(summary_item)
    print neighbourhood_summary

    neighbourhood_crime = []
    for item in neighbourhood_summary:
        headers = []
        [headers.append(key) for key in item.keys() if key != 'Month' and key != 'Force' and key != 'Neighbourhood']
        # print 'crime categories'
        # print headers
        for crime_type in headers:
            for i in xrange(int(item[crime_type])):
                # print crime_type
                row = {
                'family_id': 'TBD',
                'data_type': 'crime',
                'category': crime_type,
                'persistent_id': '',
                'month': item['Month'],
                'location_latitude': 'TBD',
                'location_longitude': 'TBD',
                'location_street_id': '',
                'location_street_name': 'TBD',
                'context': crime_type,
                'id': '',
                'location_type': 'FORCE',
                'location_subtype': '',
                'outcome_status_category': '',
                'outcome_status_date': '',
                'on_family_road': 'FALSE'
                }
                neighbourhood_crime.append(row)
    return neighbourhood_crime

# summary_neighbourhood_data = parseNeighbourhoodData()
# neighbourhood = getNeighbourhood(lat,lon)
# neighbourhood_crime = getNeighbourhoodCrime(id, lat, lon, '2013', summary_neighbourhood_data)
# print neighbourhood_crime

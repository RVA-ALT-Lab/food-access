#!/usr/bin/env python
"""This script combines the json files for each year into a single data set"""
import io
import json
import requests

COMBINED_JSON = {}
URL_BASE = 'http://census.ire.org/geo/1.0/boundary-set/tracts/'

FILE_INPUT = io.open('food-access-census-richmond.json')
FILE_RAW = FILE_INPUT.read()
PARSED_JSON = json.loads(FILE_RAW)
GEO_JSON = {
    'type': 'FeatureCollection',
    'features': []
}

# Create a dictionary of all of the cities, states, and magnitude for geocoding
for record in PARSED_JSON:

    tract = record['CensusTract']
    # create new feature dictionary
    new_feature = {
        'type': 'Feature',
        'id': tract,
        'properties': {}
    }
    # loop through properties, transfer to new geoJSON feature
    for key,value in record.items():
        new_feature['properties'][key] = value
    # get tract geometry from API
    r = requests.get(URL_BASE + '/' + tract)
    result = r.json()
    print(result)
    simple_shape = result['simple_shape']
    # reverse lat/long to long/lat to conform to geoJSON; assign back to new
    # feature
    # geoJSON_simple_shape = [[coords[1], coords[0]] for coords in simple_shape['coordinates'][0][0]]
    # result['simple_shape']['coordinates'][0] = [geoJSON_simple_shape]
    new_feature['geometry'] = result['simple_shape']
    new_feature['centroid'] = result['centroid']
    # print(new_feature)

    GEO_JSON['features'].append(new_feature)


with open('census-tracts-geojson.json', 'w') as outfile:
    json.dump(GEO_JSON, outfile)

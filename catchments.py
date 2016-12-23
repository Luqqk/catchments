# !/usr/bin/python
# -*- coding: utf-8 -*-

from optparse import OptionParser
import os.path
import csv
import requests
import json


def main():
    parser = OptionParser(usage='')
    # Required parameters
    parser.add_option('-a', '--api', type='string', help='')
    parser.add_option('-k', '--key', type='string', help='')
    parser.add_option('-f', '--file', type='string', help='')
    # Optional parameters
    parser.add_option('-r', '--range', type='int', default=600, help='')
    parser.add_option('-u', '--units', type='string', default='sec', help='')
    parser.add_option('-t', '--transport', type='string', default='car', help='')
    parser.add_option('-s', '--status', type='string', default='enabled', help='')
    
    (options, args) = parser.parse_args()

    # Validate required parameters
    if not options.api:
        parser.error('You have to choose API provider [\'SKOBBLER\', \'HERE\']')
    if options.api not in ['SKOBBLER', 'HERE']:
        parser.error('Invalid API provider [\'SKOBBLER\', \'HERE\']')
    if not options.key:
        parser.error('API KEY is required')
    if not options.file:
        parser.error('File is required (.csv with \',\' or \';\' as delimiter)')
    if not os.path.isfile(options.file):
        parser.error('File doesn\'t exist.')
    # Validate optional parameters
    if options.api == 'SKOBBLER':
        if options.units not in ['sec', 'meter']:
            parser.error('Invalid units type [\'sec\', \'meter\']')
        if options.transport not in ['pedestrian', 'bike', 'car']:
            parser.error('Invalid units type [\'pedestrian\', \'bike\', \'car\']')
    if options.api == 'HERE':
        try:
            options.app_id = options.key.split(',')[0]
            options.app_code = options.key.split(',')[1]
        except:
            parser.error('Wrong API key format')
        if not options.units or options.units not in ['time', 'distance']:
            options.units = 'time' 
        if options.units not in ['time', 'distance']:
            parser.error('Invalid units type [\'time\', \'distance\']')
        if options.transport not in ['pedestrian', 'car']:
            parser.error('Invalid units type [\'pedestrian\', \'car\']')
        if options.status not in ['enabled', 'disabled']:
            parser.error('Invalid traffic input [\'enabled\', \'disabled\']')
    
    print """Catchments params:\n
            api: {}
            key: {}
            points: {}
            range: {}
            units: {}
            transport: {}
            traffic status: {} (only for HERE)\n"""\
        .format(options.api, options.key, options.file, options.range,
                options.units, options.transport, options.status)

    # Read center points from file
    print 'Loading file with input points...'
    input_file = open(options.file)
    center_points = create_dict_reader(input_file)
    print 'Successful'
    # Get catchments (SKOBBLER or HERE) 
    if options.api == 'SKOBBLER':
        print 'Requesting catchments from SKOBBLER API...'
        for point in center_points:
            catchment = get_skobbler_catchment(point, options)
            geojson_feature = skobbler_catchment_to_geojson(catchment)
            file_name = save_as_geojson(geojson_feature, options)
            print '{} file successfully created'.format(file_name)
    else:
        print 'Requesting catchments from HERE API...'
        for point in center_points:
            catchment = get_here_catchment(point, options)
            geojson_feature = here_catchment_to_geojson(catchment)
            file_name = save_as_geojson(geojson_feature, options)
            print '{} file successfully created'.format(file_name)
    # Close input file
    input_file.close()
    return True
    

def create_dict_reader(file):
        dialect = csv.Sniffer().sniff(file.read(), delimiters=';,')
        file.seek(0)
        return csv.DictReader(file, dialect=dialect)


def get_skobbler_catchment(point, options):
    url = 'http://{0}.tor.skobbler.net/tor/RSngx/RealReach/json/20_5/en/{0}'\
        .format(options.key, options.key)
    params = {'start': '{1},{0}'.format(point['x'], point['y']),
              'transport': options.transport,
              'range': options.range,
              'units': options.units,
              'toll': 1,
              'highways': 1,
              'nonReachable': 0,
              'response_type': 'gps'}
    r = requests.get(url, params=params)
    catchment = json.loads(r.text)
    catchment['name'] = point['name']
    return catchment

def skobbler_catchment_to_geojson(catchment):
    geojson_feature = {"type": "Feature", "geometry": {
                    "type": "Polygon", "coordinates": [[]]},
                    "properties": {"name": catchment['name']}}
    coords = iter(catchment['realReach']['gpsPoints'][8:])
    for coord in coords:
        geojson_feature['geometry']['coordinates'][0].append([coord, next(coords)])
    geojson_feature['geometry']['coordinates'][0].append(
        [catchment['realReach']['gpsPoints'][8:][0],
        catchment['realReach']['gpsPoints'][8:][1]])
    return geojson_feature


def get_here_catchment(point, options):
    url = 'https://isoline.route.cit.api.here.com/routing/7.2/calculateisoline.json'
    params = {'start': 'geo!{1},{0}'.format(point['x'], point['y']),
              'mode': 'fastest;{};traffic:{}'.format(options.transport, options.status),
              'range': options.range,
              'rangetype': options.units,
              'app_id': options.app_id,
              'app_code': options.app_code}
    r = requests.get(url, params=params)
    catchment = json.loads(r.text)
    catchment['name'] = point['name']
    return catchment


def here_catchment_to_geojson(catchment):
    geojson_feature = {"type": "Feature",
                    "geometry": {"type": "Polygon", "coordinates": [[]]},
                    "properties": {"name": catchment['name']}}
    crds = []
    for row in catchment['response']['isoline'][0]['component'][0]['shape']:
        splt = row.split(',')
        crds.append(float(splt[1]))
        crds.append(float(splt[0]))
    coords = iter(crds)
    for coord in coords:
        geojson_feature['geometry']['coordinates'][0].append([coord, next(coords)])
    geojson_feature['geometry']['coordinates'][0].append([crds[0], crds[1]])
    return geojson_feature


def save_as_geojson(feature, options):
    file_name = feature['properties']['name'].lower().replace(' ', '_')
    file_suffix = '_{}_{}_{}_{}.geojson'\
        .format(options.transport, options.range, options.units, options.api)
    with open('{0}{1}'.format(file_name, file_suffix), 'w') as file_:
        file_.write(json.dumps(feature, indent=2))
    return file_name + file_suffix

      
if __name__ == '__main__':
    main()

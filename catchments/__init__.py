import os
import json
import requests
from functools import wraps
from datetime import datetime


def validate_required_params(*params):
    
    def func_decorator(func):
        
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            
            if not all(param in kwargs.keys() for param in params):
                raise ValueError('Required params not supplied')
            
            if kwargs['api'] not in ('SKOBBLER', 'HERE'):
                raise ValueError('Only SKOBBLER or HERE allowed')

            return func(*args, **kwargs)
        
        return wrapped_function
    
    return func_decorator


@validate_required_params('api', 'key')
def request_catchment(point, **params):

    req_params = {}

    if params['api'] == 'SKOBBLER':

        url = 'http://{}.tor.skobbler.net/tor/RSngx/RealReach/json/20_5/en/{}'.format(
            params['key'],params['key']
        )
        
        req_params['start'] = '{1},{0}'.format(point['lon'], point['lat'])
        
        req_params['transport'] = params.get('transport', 'car')
        
        req_params['range'] = params.get('range', 600)
        
        req_params['units'] = params.get('units', 'sec')
        
        req_params['toll'] = params.get('toll', 1)
        
        req_params['highways'] = params.get('highways', 1)
        
        req_params['nonReachable'] = params.get('non_reachable', 0)
        
        req_params['response_type'] = 'gps'
    
    elif params['api'] == 'HERE':

        url = 'https://isoline.route.cit.api.here.com/routing/7.2/calculateisoline.json'
        
        req_params['start'] = 'geo!{1},{0}'.format(point['lon'], point['lat'])
        
        req_params['mode'] = 'fastest;{};traffic:{}'.format(
            params.get('transport', 'car'),
            params.get('traffic', 'disabled')
        )
        
        req_params['range'] = params.get('range', 600)
        
        req_params['rangetype'] = params.get('units', 'time')
        
        req_params['app_id'] = params['key'].split(',')[0]
        
        req_params['app_code'] = params['key'].split(',')[1]
    
    else:
        raise ValueError('Non supported API')

    try:
        r = requests.get(url, params=req_params)
        r.raise_for_status()
    except requests.HTTPError:
        return False

    # TODO Validate if response has coords

    catchment = r.json()

    catchment['name'] = point.get(
            'name',
            '{}_{}'.format(point['lat'], point['lon'])
        )

    return catchment


@validate_required_params('api')
def catchment_as_geojson(catchment, **params):
    
    geojson_feature = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon", "coordinates": [[]]
        },
        "properties": {}
    }

    if params['api'] == 'SKOBBLER':
        
        coords = catchment['realReach']['gpsPoints']
        bbox = catchment['realReach']['gpsBBox']
        
        for i, coord in enumerate(coords):
            if (i % 2 == 0):
                if not (coord < bbox[0] or coord > bbox[2]):
                    geojson_feature['geometry']['coordinates'][0].append(
                        [coord, coords[i + 1]]
                    )
    
    elif params['api'] == 'HERE':
        
        shape = catchment['response']['isoline'][0]['component'][0]['shape']
        coords = []

        for coord in shape:
            lat_lon = coord.split(',')
            coords.append(float(lat_lon[1]))
            coords.append(float(lat_lon[0]))

        for i, coord in enumerate(coords):
            if (i % 2 == 0):
                geojson_feature['geometry']['coordinates'][0].append(
                    [coord, coords[i + 1]]
                )

    else:
        raise ValueError('Non supported API')

    # Close geojson polygon
    geojson_feature['geometry']['coordinates'][0].append(
        geojson_feature['geometry']['coordinates'][0][0]
    )

    geojson_feature['properties']['name'] = catchment['name']
    
    return geojson_feature


@validate_required_params('api')
def save_as_geojson(geo_feature, **params):

    name = '{}_{}.geojson'.format(
            params['api'], 
            geo_feature['properties']['name']
        )

    feature = json.dumps(geo_feature, indent=2)

    with open(name, 'w') as f:
        f.write(feature)

    return name


def create_parser():
    
    parser = OptionParser(usage='')
    
    # Required parameters
    
    parser.add_option(
        '-a', '--api', type='choice', choices=['HERE', 'SKOBBLER'],
        help=''
    )
    parser.add_option(
        '-k', '--key', type='string',
        help=''
    )
    parser.add_option(
        '-p', '--points', type='string',
        help=''
    )
    
    # Optional parameters
    
    parser.add_option(
        '-r', '--range', type='int', default=600,
        help=''
    )
    parser.add_option('-u', '--units', type='choice',
        choices=['sec', 'meter', 'time', 'distance'], default='sec',
        help=''
    )
    parser.add_option('-t', '--transport', type='choice',
        choices=['pedestrian', 'bike', 'car'], default='car',
        help=''
    )
    parser.add_option(
        '-tf', '--traffic', type='choice',
        choices=['enabled', 'disabled'], default='enabled',
        help=''
    )

    return parser


def load_input_data(points):

    dialect = csv.Sniffer().sniff(points.read())
    
    points.seek(0)

    data = csv.DictReader(file, dialect=dialect)
    
    return data

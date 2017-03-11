import os
import csv
import json
import requests
from functools import wraps
from optparse import OptionParser


def validate_required_params(*params):
    """Validates function required parameters.

    Args:
        *params: key name (string) which has to be included in parameters
    
    Returns:
        decorated function if success

    Raises:
        ValueError if required param is not supplied

    Examples:
        Check if 'api' key exists in function parameters.
        
        >>>@validate_required_params('api')
        >>>function_to_validate(api='example'):
               return True

    """
    
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
    """Requests catchment from chosen API provider.

    Args:
        point (dictionary): {'name': 'place', 'lon': 50.0, 'lat': 20.0}
            'name' key is optional, 'lon' and 'lat' are required
        **params: [
                api (required), key (required), transport, range,
                units, toll, highways, non_reachable, jam
            ]
            If optional params won't be supplied, default values will be used
    
    Returns:
        dictionary: api response if successful, None otherwise

    Raises:
        ValueError if required param is not supplied

    Examples:
        Get catchment from SKOBBLER API for specified point.

        >>>catchment = request_catchment({'lon': 50.0, 'lat': 20.0}, api='SKOBBLER', key='api_key')

    """

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
    
    else: # HERE API

        url = 'https://isoline.route.cit.api.here.com/routing/7.2/calculateisoline.json'
        
        req_params['start'] = 'geo!{1},{0}'.format(point['lon'], point['lat'])
        
        req_params['mode'] = 'fastest;{};traffic:{}'.format(
            params.get('transport', 'car'),
            params.get('jam', 'disabled')
        )
        
        req_params['range'] = params.get('range', 600)
        
        req_params['rangetype'] = params.get('units', 'time')
        
        req_params['app_id'] = params['key'].split(',')[0]
        
        req_params['app_code'] = params['key'].split(',')[1]

    try:
        r = requests.get(url, params=req_params)
        r.raise_for_status()
    except requests.HTTPError:
        return None

    catchment = r.json()

    catchment['name'] = point.get(
            'name',
            '{}_{}'.format(point['lat'], point['lon'])
        )

    return catchment


@validate_required_params('api')
def catchment_as_geojson(catchment, **params):
    """Processing catchment to GeoJSON format.

    Args:
        catchment (dictionary): output from request_catchment function
        **params: [api (required)]
    
    Returns:
        dictionary: GeoJSON polygon feature if successful, None otherwise

    Raises:
        ValueError if required param is not supplied

    Examples:
        Process catchment to GeoJSON.

        >>>geojson = catchment_as_geojson(valid_catchment_object, api='SKOBBLER')

    """
    
    geojson_feature = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon", "coordinates": [[]]
        },
        "properties": {}
    }

    if params['api'] == 'SKOBBLER':

        try:
            coords = catchment['realReach']['gpsPoints']
            bbox = catchment['realReach']['gpsBBox']
        except KeyError:
            return None
        
        for i, coord in enumerate(coords):
            if (i % 2 == 0):
                if not (coord < bbox[0] or coord > bbox[2]):
                    geojson_feature['geometry']['coordinates'][0].append(
                        [coord, coords[i + 1]]
                    )
        # Close GeoJSON polygon (Only SKOBBLER)
        geojson_feature['geometry']['coordinates'][0].append(
            geojson_feature['geometry']['coordinates'][0][0]
        )
    
    else: # HERE API

        try:
            shape = catchment['response']['isoline'][0]['component'][0]['shape']
        except KeyError:
            return None
        
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

    geojson_feature['properties']['name'] = catchment['name']
    
    return geojson_feature


@validate_required_params('api')
def save_as_geojson(geo_feature, save_in=None, **params):
    """Save GeoJSON feature to *.geojson file

    Args:
        geo_feature (dictionary): valid GeoJSON feature object
        save_in (path): path where to save generated files
        **params: [api (required)]
    
    Returns:
        file: GeoJSON feature
        path_to_save: saved *.geojson file path

    Raises:
        ValueError if required param is not supplied

    Examples:
        Save GeoJSON feature to file.

        >>>file_path = save_as_geojson(valid_geojson_feature, api='SKOBBLER')

    """

    name = '{}_{}.geojson'.format(
            params['api'], 
            geo_feature['properties']['name']
        )
    
    if save_in:
        path_to_save = os.path.join(save_in, name)
    else:
        path_to_save = os.path.join(os.getcwd(), name)

    feature = json.dumps(geo_feature, indent=2)

    with open(path_to_save, 'w') as f:
        f.write(feature)

    return path_to_save


def create_parser():
    """Creates parser for commandline arguments.
    
    Returns:
        parser (optparse.OptionParser)

    Examples:
        Create parser.

        >>>parser = create_parser()

    """
    
    parser = OptionParser()
    
    # Required parameters
    
    parser.add_option(
        '-a', '--api', type='choice', choices=['HERE', 'SKOBBLER'],
        help='API provider (SKOBBLER, HERE)'
    )
    parser.add_option(
        '-k', '--key', type='string',
        help='SKOBBLER or HERE API key'
    )
    parser.add_option(
        '-p', '--points', type='string',
        help='*.csv file to read points from'
    )
    
    # Optional parameters
    
    parser.add_option(
        '-r', '--range', type='int', default=600,
        help='Range (int)'
    )
    parser.add_option('-u', '--units', type='choice',
        choices=['sec', 'meter', 'time', 'distance'], default='sec',
        help='Units (sec, meter, time, distance)'
    )
    parser.add_option('-t', '--transport', type='choice',
        choices=['pedestrian', 'bike', 'car'], default='car',
        help='Transport type (pedestrian, bike, car)'
    )
    parser.add_option(
        '-j', '--jam', type='choice',
        choices=['enabled', 'disabled'], default='enabled',
        help='Real time traffic (enabled, disabled)'
    )

    return parser


def load_input_data(points):
    """Creates DictReader from *.csv file.

    Args:
        points (file object): *.csv file with 'lon' (required),
            'lat' (required), 'name' (optional) columns
    
    Returns:
        data (csv.DictReader)

    Examples:
        Load example.csv file

        >>>load_input_data('/path/to/example.csv')

    """

    dialect = csv.Sniffer().sniff(points.read())
    
    points.seek(0)

    data = csv.DictReader(points, dialect=dialect)
    
    return data

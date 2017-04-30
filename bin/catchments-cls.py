#!/usr/bin/python

import os.path
from catchments import SkobblerAPI, HereAPI
from catchments.utils import create_parser, load_input_data


def main():
    """Get catchments for points in given file.

    Command line script for acquiring and creating
    GeoJSON files from given file input.

    """

    parser = create_parser()

    (options, args) = parser.parse_args()
    params = vars(options)

    for param in ['api', 'key', 'points']:
        if params[param] is None:
            parser.error('Missing required param')

    if not os.path.isfile(params['points']):
        parser.error('File doesn\'t exist')
    
    if params['api'] == 'SKOBBLER':
        api_provider = SkobblerAPI(params['key'])
    else:
        app_id = params['key'].split(',')[0]
        app_code = params['key'].split(',')[1]
        api_provider = HereAPI(app_id, app_code)

    file = open(params['points'])

    points = load_input_data(file)

    for point in points:

        catchment = api_provider.get_catchment(point, **params)

        if catchment:
            geojson_feature = api_provider.catchment_as_geojson(catchment)
            if geojson_feature:
                file_path = api_provider.save_as_geojson(geojson_feature)
                print('{} file has been created.'.format(file_path))
            else:
                print('Couldn\'t proccess catchment for {},{} to GeoJSON (Invalid API response)'.format(
                    point['lat'], point['lon']
                ))
        else:
            print('Couldn\'t get catchment for {},{} coordinates (HTTP Error).'.format(
                point['lat'], point['lon'])
            )

    file.close()

if __name__ == '__main__':
    main()

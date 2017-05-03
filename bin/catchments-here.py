#!/usr/bin/python

import os.path
from catchments import HereAPI
from catchments.parsers import create_here_parser
from catchments.utils import load_input_data


def main():
    """Get catchments for points in given file
    from Skobbler RealReach API.

    Command line script for acquiring and creating
    GeoJSON files from given file input.

    """

    parser = create_here_parser()

    (options, args) = parser.parse_args()
    params = vars(options)

    for param in ['app_id', 'app_code', 'points']:
        if params[param] is None:
            parser.error('Missing required param')

    if not os.path.isfile(params['points']):
        parser.error('File doesn\'t exist')
    
    here_api = HereAPI(params['app_id'], params['app_code'])

    file = open(params['points'])

    points = load_input_data(file)

    for point in points:

        catchment = here_api.get_catchment(point, **params)

        if catchment:
            geojson_feature = here_api.catchment_as_geojson(catchment)
            if geojson_feature:
                file_path = here_api.save_as_geojson(geojson_feature)
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

#!/usr/bin/python

import os.path
from catchments import create_parser, load_input_data, request_catchment, \
    catchment_as_geojson, save_as_geojson


def main():
    """Get catchments for points in given file.

    Command line script for acquiring and creating
    GeoJSON files from given file input.

    """

    parser = create_parser()

    (options, args) = parser.parse_args()
    params = vars(options)

    if not os.path.isfile(params['points']):
        parser.error('File doesn\'t exist')

    file = open(params['points'])

    points = load_input_data(file)

    for point in points:

        catchment = request_catchment(point, **params)

        if catchment:
            geojson_feature = catchment_as_geojson(catchment, **params)
            if geojson_feature:
                file_path = save_as_geojson(geojson_feature, **params)
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

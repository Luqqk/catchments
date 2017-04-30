import os
import csv
import json
import requests


class HereAPI(object):
    """The HereAPI object implements HERE Isolines API."""

    def __init__(self, app_id, app_code):
        self.app_id = app_id
        self.app_code = app_code

    def _request(self, url, point, params):
        try:
            r = requests.get(url, params=params)
            r.raise_for_status()
        except requests.HTTPError:
            return None

        catchment = r.json()

        catchment['name'] = point.get(
            'name', '{}_{}'.format(point['lat'], point['lon'])
        )

        return catchment

    def get_catchment(self, point, **params):
        """Requests catchment from API provider.

        :param point (dictionary): {'name': 'place', 'lon': 50.0, 'lat': 20.0}
            'name' key is optional, 'lon' and 'lat' are required.

        :param params (**dictionary):
                supported keys:
                    mode, range, rangetype

        If optional params won't be supplied, default values will be used.

        Returns:
            API response if successful, None otherwise.
        """

        url = 'https://isoline.route.cit.api.here.com/routing/7.2/calculateisoline.json'

        request_params = {}

        request_params['start'] = 'geo!{1},{0}'.format(point['lon'], point['lat'])

        request_params['mode'] = params.get('mode', 'fastest;car;traffic:disabled')

        request_params['range'] = params.get('range', 600)

        request_params['rangetype'] = params.get('rangetype', 'time')

        request_params['app_id'] = self.app_id

        request_params['app_code'] = self.app_code

        return self._request(url, point, request_params)

    @staticmethod
    def catchment_as_geojson(catchment):
        """Processing catchment to GeoJSON format.

        :param catchment (dictionary)

        Returns:
            GeoJSON polygon feature if successful, None otherwise.
        """

        geojson = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon", "coordinates": [[]]
            },
            "properties": {}
        }

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
                geojson['geometry']['coordinates'][0].append(
                    [coord, coords[i + 1]]
                )

        geojson['properties']['name'] = catchment['name']

        return geojson

    @staticmethod
    def save_as_geojson(geojson, save_in=None):
        """Save GeoJSON feature to *.geojson file.

        :param geojson (dictionary - GeoJSON feature)

        :param save_in (path)

        Returns:
           File with GeoJSON feature
           path_to_save: saved *.geojson file path
        """

        name = 'HERE_{}.geojson'.format(geojson['properties']['name'])

        if save_in:
            path_to_save = os.path.join(save_in, name)
        else:
            path_to_save = os.path.join(os.getcwd(), name)

        feature = json.dumps(geojson, indent=2)

        with open(path_to_save, 'w') as f:
            f.write(feature)

        return path_to_save

import os
import csv
import json
import requests


class SkobblerAPI(object):
    """The SkobblerAPI object implements Skobbler RealReach API."""

    def __init__(self, api_key):
        self.api_key = api_key

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

        :param point (dictionary):
            {'name': 'place', 'lon': 50.0, 'lat': 20.0}
            'name' key is optional, 'lon' and 'lat' are required.

        :param params (**dictionary):
                supported keys:
                    transport, range, units, toll, highways, non_reachable, jam

        If optional params won't be supplied, default values will be used.

        Returns:
            API response if successful, None otherwise.
        """

        url = 'http://{}.tor.skobbler.net/tor/RSngx/RealReach/json/20_5/en/{}'.format(
            self.api_key, self.api_key
        )

        request_params = {}

        request_params['start'] = '{1},{0}'.format(point['lon'], point['lat'])

        request_params['transport'] = params.get('transport', 'car')

        request_params['range'] = params.get('range', 600)

        request_params['units'] = params.get('units', 'sec')

        request_params['toll'] = params.get('toll', '0')

        request_params['highways'] = params.get('highways', '0')

        request_params['nonReachable'] = params.get('non_reachable', '0')

        request_params['response_type'] = 'gps'

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
            coords = catchment['realReach']['gpsPoints']
            bbox = catchment['realReach']['gpsBBox']
        except KeyError:
            return None

        for i, coord in enumerate(coords):
            if (i % 2 == 0):
                if not (coord < bbox[0] or coord > bbox[2]):
                    geojson['geometry']['coordinates'][0].append(
                        [coord, coords[i + 1]]
                    )
        # Close GeoJSON polygon
        geojson['geometry']['coordinates'][0].append(
            geojson['geometry']['coordinates'][0][0]
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

        name = 'SKOBBLER_{}.geojson'.format(geojson['properties']['name'])

        if save_in:
            path_to_save = os.path.join(save_in, name)
        else:
            path_to_save = os.path.join(os.getcwd(), name)

        feature = json.dumps(geojson, indent=2)

        with open(path_to_save, 'w') as f:
            f.write(feature)

        return path_to_save

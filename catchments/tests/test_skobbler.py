from unittest import TestCase
from unittest.mock import patch, Mock
from io import StringIO
from tempfile import mkdtemp
from shutil import rmtree
from catchments import SkobblerAPI
from .test_data import EXAMPLE_SKOBBLER_PARAMS, EXAMPLE_SKOBBLER_CATCHMENT, \
    EXAMPLE_SKOBBLER_GEOJSON
import os
import csv
import requests
# csv.OrderedDict is supported only in Python > 3.6
# collections.OrderedDict for backward compatibility (Python < 3.6)
import collections


# Run tests with:
# coverage run --branch --source=catchments/ setup.py test
# To check coverage report (with missing lines)
# coverage report -m


class TestRequestSkobblerCatchment(TestCase):

    def setUp(self):
        self.skobbler_api = SkobblerAPI('api_key')
        self.skobbler_point = {'lat': 50.0, 'lon': 16.0}
        # Construct mock response object
        self.skobbler_mock_response = Mock()

    @patch('requests.get')
    def test_request_skobbler_catchment(self, mock_request):
        successful_skobbler_response = {
            "realReach": {
                "gpsPoints": []
            }
        }
        # Assign mock response as the result of patched function
        self.skobbler_mock_response.json.return_value = successful_skobbler_response
        mock_request.return_value = self.skobbler_mock_response

        self.assertEqual(
            self.skobbler_api.get_catchment(self.skobbler_point, **EXAMPLE_SKOBBLER_PARAMS), 
            successful_skobbler_response
        )
    
    @patch('requests.get')
    def test_request_skobbler_catchment_http_error(self, mock_request):
        skobbler_http_error_response = {}

        http_error = requests.exceptions.HTTPError()
        
        self.skobbler_mock_response.json.return_value = skobbler_http_error_response
        self.skobbler_mock_response.raise_for_status.side_effect = http_error
        mock_request.return_value = self.skobbler_mock_response
        self.assertEqual(self.skobbler_api.get_catchment(self.skobbler_point, **EXAMPLE_SKOBBLER_PARAMS), None)


class TestSkobblerCatchmentAsGeojson(TestCase):

    def setUp(self):
        self.skobbler_api = SkobblerAPI('api_key')
        self.skobbler_catchment = EXAMPLE_SKOBBLER_CATCHMENT
        self.skobbler_geojson = EXAMPLE_SKOBBLER_GEOJSON
        self.skobbler_geojson_feature = self.skobbler_api.catchment_as_geojson(
            EXAMPLE_SKOBBLER_CATCHMENT
        )

    def test_skobbler_catchment_as_geojson(self):
        self.assertEqual(self.skobbler_geojson_feature, self.skobbler_geojson)
    
    def test_skobbler_catchment_name(self):
        self.assertEqual(
            self.skobbler_geojson_feature['properties']['name'],
            self.skobbler_geojson['properties']['name']
        )
    
    def test_skobbler_invalid_api_response(self):
        invalid_skobbler_response = {"status": {"httpCode": 401}}
        self.assertEqual(
            self.skobbler_api.catchment_as_geojson(invalid_skobbler_response),
            None
        )


class TestSaveAsGeojson(TestCase):

    def setUp(self):
        self.skobbler_api = SkobblerAPI('api_key')
        self.params = EXAMPLE_SKOBBLER_PARAMS
        # Create a temporary directory
        self.test_dir = mkdtemp()
        self.geojson = EXAMPLE_SKOBBLER_GEOJSON

    def tearDown(self):
        # Remove the directory after the test
        rmtree(self.test_dir)

    def test_save_as_geojson_with_save_in(self):
        path_to_save = self.skobbler_api.save_as_geojson(self.geojson, save_in=self.test_dir)
        self.assertEqual(path_to_save, os.path.join(self.test_dir, 'SKOBBLER_test_point.geojson'))
    
    def test_save_as_geojson(self):
        path_to_save = self.skobbler_api.save_as_geojson(self.geojson)
        os.remove(path_to_save)
        self.assertEqual(path_to_save, os.path.join(os.getcwd(), 'SKOBBLER_test_point.geojson'))

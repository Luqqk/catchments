from unittest import TestCase
from unittest.mock import patch, Mock
from optparse import OptionParser
from io import StringIO
from tempfile import mkdtemp
from shutil import rmtree
from catchments import HereAPI
from .test_data import EXAMPLE_HERE_PARAMS, EXAMPLE_HERE_CATCHMENT, \
    EXAMPLE_HERE_GEOJSON
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


class TestRequestHereCatchment(TestCase):

    def setUp(self):
        self.here_api = HereAPI('app_id', 'app_code')
        self.here_point = {'lat': 50.0, 'lon': 16.0}
        self.here_mock_response = Mock()

    @patch('requests.get')
    def test_request_here_catchment(self, mock_request):
        successful_here_response = {
            "response": {
                "isoline": [
                    {"component": [
                            {"shape": []}
                        ]
                    }
                ]
            }
        }
        
        self.here_mock_response.json.return_value = successful_here_response
        mock_request.return_value = self.here_mock_response

        self.assertEqual(
            self.here_api.get_catchment(self.here_point, **EXAMPLE_HERE_PARAMS),
            successful_here_response
        )

    @patch('requests.get')
    def test_request_here_catchment_http_error(self, mock_request):
        skobbler_http_error_response = {}

        http_error = requests.exceptions.HTTPError()
        
        self.here_mock_response.json.return_value = skobbler_http_error_response
        self.here_mock_response.raise_for_status.side_effect = http_error
        mock_request.return_value = self.here_mock_response
        self.assertEqual(self.here_api.get_catchment(self.here_point, **EXAMPLE_HERE_PARAMS), None)


class TestHereCatchmentAsGeojson(TestCase):

    def setUp(self):
        self.here_api = HereAPI('app_id', 'app_code')
        self.here_geojson = EXAMPLE_HERE_GEOJSON
        self.here_geojson_feature = self.here_api.catchment_as_geojson(
            EXAMPLE_HERE_CATCHMENT
        )

    def test_here_catchment_as_geojson(self):
        self.assertEqual(self.here_geojson_feature, self.here_geojson)
    
    def test_here_invalid_api_response(self):
        invalid_here_response = {"response": {"type": "PermissionError"}}
        self.assertEqual(
            self.here_api.catchment_as_geojson(invalid_here_response),
            None
        )

class TestSaveAsGeojson(TestCase):

    def setUp(self):
        self.here_api = HereAPI('app_id', 'app_code')
        self.params = EXAMPLE_HERE_PARAMS
        # Create a temporary directory
        self.test_dir = mkdtemp()
        self.geojson = EXAMPLE_HERE_GEOJSON

    def tearDown(self):
        # Remove the directory after the test
        rmtree(self.test_dir)

    def test_save_as_geojson_with_save_in(self):
        path_to_save = self.here_api.save_as_geojson(self.geojson, save_in=self.test_dir)
        self.assertEqual(path_to_save, os.path.join(self.test_dir, 'HERE_test_point.geojson'))
    
    def test_save_as_geojson(self):
        path_to_save = self.here_api.save_as_geojson(self.geojson)
        os.remove(path_to_save)
        self.assertEqual(path_to_save, os.path.join(os.getcwd(), 'HERE_test_point.geojson'))

from unittest import TestCase
from unittest.mock import patch, Mock
from optparse import OptionParser
from io import StringIO
from tempfile import mkdtemp
from shutil import rmtree
from catchments import create_parser, load_input_data, request_catchment, \
    catchment_as_geojson, save_as_geojson, validate_required_params
from .test_data import EXAMPLE_SKOBBLER_PARAMS, EXAMPLE_HERE_PARAMS, \
    EXAMPLE_SKOBBLER_CATCHMENT, EXAMPLE_SKOBBLER_GEOJSON, \
    EXAMPLE_HERE_CATCHMENT, EXAMPLE_HERE_GEOJSON
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


class TestParser(TestCase):

    def test_parser_creation(self):
        parser = create_parser()
        self.assertTrue(isinstance(parser, OptionParser))


class TestLoadInputData(TestCase):

    def setUp(self):
        self.data_temp = StringIO()
        dict_writer = csv.DictWriter(self.data_temp, fieldnames=['lat', 'lon'])
        dict_writer.writeheader()
        dict_writer.writerow({'lat': 52.02, 'lon': 16.02})
        self.data_temp.seek(0)
    
    def test_load_csv(self):   
        data = load_input_data(self.data_temp)
        self.assertTrue(isinstance(data, csv.DictReader))

    def test_data_output(self):
        data = load_input_data(self.data_temp)
        for row in data:
            self.assertEqual(row, collections.OrderedDict([('lat', '52.02'), ('lon', '16.02')]))
    

class TestValidateDecorator(TestCase):

    def setUp(self):

        @validate_required_params('api', 'key')
        def func(**params):
            return True
        
        self.func_to_validate = func
    
    def test_successful_validation(self):
        self.assertEqual(self.func_to_validate(**EXAMPLE_SKOBBLER_PARAMS), True)
    
    def test_failed_validation(self):
        self.assertEqual(self.func_to_validate(**EXAMPLE_SKOBBLER_PARAMS), True)
        missing_required_param = {'api': 'SKOBBLER'}
        self.assertRaises(ValueError, self.func_to_validate, **missing_required_param)
    
    def test_unsupported_api_value_in_params(self):
        self.assertEqual(self.func_to_validate(**EXAMPLE_SKOBBLER_PARAMS), True)
        wrong_api_params = {'api': 'MAPZEN', 'key': 'your_api_key'}
        self.assertRaises(ValueError, self.func_to_validate, **wrong_api_params)


class TestRequestSkobblerCatchment(TestCase):

    def setUp(self):
        self.skobbler_point = {'lat': 50.0, 'lon': 16.0}
        # Construct mock response object
        self.skobbler_mock_response = Mock()
    
    @patch('requests.get')
    def test_request_catchment_wrong_api(self, mock_request):
        wrong_skobbler_params = {'api': 'MAPZEN', 'key': 'your_api_key'}
        self.assertRaises(ValueError, request_catchment, self.skobbler_point, **wrong_skobbler_params)

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
            request_catchment(self.skobbler_point, **EXAMPLE_SKOBBLER_PARAMS), 
            successful_skobbler_response
        )
    
    @patch('requests.get')
    def test_request_skobbler_catchment_http_error(self, mock_request):
        skobbler_http_error_response = {}

        http_error = requests.exceptions.HTTPError()
        
        self.skobbler_mock_response.json.return_value = skobbler_http_error_response
        self.skobbler_mock_response.raise_for_status.side_effect = http_error
        mock_request.return_value = self.skobbler_mock_response
        self.assertEqual(request_catchment(self.skobbler_point, **EXAMPLE_SKOBBLER_PARAMS), None)


class TestRequestHereCatchment(TestCase):

    def setUp(self):
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
            request_catchment(self.here_point, **EXAMPLE_HERE_PARAMS),
            successful_here_response
        )


class TestSkobblerCatchmentAsGeojson(TestCase):

    def setUp(self):
        self.skobbler_catchment = EXAMPLE_SKOBBLER_CATCHMENT
        self.skobbler_geojson = EXAMPLE_SKOBBLER_GEOJSON
        self.skobbler_geojson_feature = catchment_as_geojson(
            EXAMPLE_SKOBBLER_CATCHMENT, **EXAMPLE_SKOBBLER_PARAMS
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
            catchment_as_geojson(invalid_skobbler_response, **EXAMPLE_SKOBBLER_PARAMS),
            None
        )


class TestHereCatchmentAsGeojson(TestCase):

    def setUp(self):
        self.here_geojson = EXAMPLE_HERE_GEOJSON
        self.here_geojson_feature = catchment_as_geojson(
            EXAMPLE_HERE_CATCHMENT, **EXAMPLE_HERE_PARAMS
        )

    def test_here_catchment_as_geojson(self):
        self.assertEqual(self.here_geojson_feature, self.here_geojson)
    
    def test_here_invalid_api_response(self):
        invalid_here_response = {"response": {"type": "PermissionError"}}
        self.assertEqual(
            catchment_as_geojson(invalid_here_response, **EXAMPLE_HERE_PARAMS),
            None
        )


class TestSaveAsGeojson(TestCase):

    def setUp(self):
        self.params = EXAMPLE_SKOBBLER_PARAMS
        # Create a temporary directory
        self.test_dir = mkdtemp()
        self.geojson = EXAMPLE_SKOBBLER_GEOJSON

    def tearDown(self):
        # Remove the directory after the test
        rmtree(self.test_dir)

    def test_save_as_geojson_with_save_in(self):
        path_to_save = save_as_geojson(self.geojson, save_in=self.test_dir, **self.params)
        self.assertEqual(path_to_save, os.path.join(self.test_dir, 'SKOBBLER_test_point.geojson'))
    
    def test_save_as_geojson(self):
        path_to_save = save_as_geojson(self.geojson, **self.params)
        os.remove(path_to_save)
        self.assertEqual(path_to_save, os.path.join(os.getcwd(), 'SKOBBLER_test_point.geojson'))

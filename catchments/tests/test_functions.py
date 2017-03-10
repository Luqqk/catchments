from unittest import TestCase
from unittest.mock import patch, Mock
from optparse import OptionParser
from io import StringIO
from tempfile import mkdtemp
from shutil import rmtree
from catchments import create_parser, load_input_data, request_catchment, \
    catchment_as_geojson, save_as_geojson, validate_required_params
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
        self.params = {'api': 'SKOBBLER', 'key': 'your_api_key'}

        @validate_required_params('api', 'key')
        def func(**params):
            return True
        
        self.func_to_validate = func
    
    def test_successful_validation(self):
        self.assertEqual(self.func_to_validate(**self.params), True)
    
    def test_failed_validation(self):
        self.assertEqual(self.func_to_validate(**self.params), True)
        del self.params['key']
        self.assertRaises(ValueError, self.func_to_validate, **self.params)
    
    def test_unsupported_api_value_in_params(self):
        self.assertEqual(self.func_to_validate(**self.params), True)
        self.params['api'] = 'MAPZEN'
        self.assertRaises(ValueError, self.func_to_validate, **self.params)


class TestRequestSkobblerCatchment(TestCase):

    def setUp(self):
        self.params = {'api': 'SKOBBLER', 'key': 'your_api_key'}
        self.point = {'lat': 50.0, 'lon': 16.0}
    
    @patch('requests.get')
    def test_request_catchment_wrong_api(self, mock_request):
        self.params['api'] = 'MAPZEN'
        self.assertRaises(ValueError, request_catchment, self.point, **self.params)

    @patch('requests.get')
    def test_request_skobbler_catchment(self, mock_request):
        # Construct mock response object
        mock_response = Mock()
        
        expected_response = {
            "realReach": {
                "gpsPoints": []
            }
        }
        # Assign mock response as the result of patched function
        mock_response.json.return_value = expected_response
        mock_request.return_value = mock_response

        self.assertEqual(request_catchment(self.point, **self.params), expected_response)
    
    @patch('requests.get')
    def test_request_skobbler_catchment_http_error(self, mock_request):
        mock_response = Mock()
        
        expected_response = {}

        http_error = requests.exceptions.HTTPError()
        
        mock_response.json.return_value = expected_response
        mock_response.raise_for_status.side_effect = http_error
        mock_request.return_value = mock_response
        self.assertEqual(request_catchment(self.point, **self.params), False)
    
    @patch('requests.get')
    def test_request_skobbler_empty_catchment(self, mock_request):
        mock_response = Mock()
        
        expected_response = {}
        
        mock_response.json.return_value = expected_response
        mock_request.return_value = mock_response

        self.assertEqual(request_catchment(self.point, **self.params), False)


class TestRequestHereCatchment(TestCase):

    def setUp(self):
        self.params = {'api': 'HERE', 'key': 'your_api_id,your_app_code'}
        self.point = {'lat': 50.0, 'lon': 16.0}
    
    @patch('requests.get')
    def test_request_catchment_wrong_api(self, mock_request):
        self.params['api'] = 'MAPZEN'
        self.assertRaises(ValueError, request_catchment, self.point, **self.params)

    @patch('requests.get')
    def test_request_here_catchment(self, mock_request):
        mock_response = Mock()

        #expected_response = {"response":["isoline":["component":["shape":[]]]]}
        expected_response = {
            "response": {
                "isoline": [
                    {"component": [
                            {"shape": []}
                        ]
                    }
                ]
            }
        }
        
        mock_response.json.return_value = expected_response
        mock_request.return_value = mock_response

        self.assertEqual(request_catchment(self.point, **self.params), expected_response)
    
    @patch('requests.get')
    def test_request_here_catchment_http_error(self, mock_request):
        mock_response = Mock()
        
        expected_response = {}

        http_error = requests.exceptions.HTTPError()
        
        mock_response.json.return_value = expected_response
        mock_response.raise_for_status.side_effect = http_error
        mock_request.return_value = mock_response
        self.assertEqual(request_catchment(self.point, **self.params), False)
    
    @patch('requests.get')
    def test_request_here_empty_catchment(self, mock_request):
        mock_response = Mock()
        
        expected_response = {}
        
        mock_response.json.return_value = expected_response
        mock_request.return_value = mock_response

        self.assertEqual(request_catchment(self.point, **self.params), False)


class TestSkobblerCatchmentAsGeojson(TestCase):

    def setUp(self):
        self.params = {'api': 'SKOBBLER'}
        self.catchment = {
            "realReach": {
                "gpsBBox": [10.00,45.00,16.00,52.00],
                "gpsPoints": [
                    -180.0,85.051129,
                    180.0,85.051129,
                    180.0,-85.051129,
                    -180.0,-85.051129,
                    10.10,45.20,
                    11.10,46.20,
                    12.10,47.20,
                    13.10,48.20,
                    14.10,49.20,
                    15.10,50.20
                ]
            },
            "name": "test_point"
        }
        self.geojson = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [10.10,45.20],
                        [11.10,46.20],
                        [12.10,47.20],
                        [13.10,48.20],
                        [14.10,49.20],
                        [15.10,50.20],
                        [10.10,45.20]
                    ]
                ]
            },
            "properties": {
                "name": "test_point"
            }
        }

    def test_skobbler_catchment_as_geojson(self):
        geojson_feature = catchment_as_geojson(self.catchment, **self.params)
        self.assertEqual(geojson_feature, self.geojson)
    
    def test_skobbler_catchment_name(self):
        geojson_feature = catchment_as_geojson(self.catchment, **self.params)
        self.assertEqual(geojson_feature['properties']['name'], self.geojson['properties']['name'])


class TestHereCatchmentAsGeojson(TestCase):

    def setUp(self):
        "50.3827858,16.9758511"
        self.params = {'api': 'HERE'}
        self.catchment = {
            "response": {
                "isoline": [
                    {"component": [
                            {"shape": [
                                    "50.00,16.00",
                                    "50.10,16.10",
                                    "50.20,16.20",
                                    "50.30,16.30",
                                    "50.00,16.00",
                                ]
                            }
                        ]
                    }
                ]
            },
            "name": "test_point"
        }
        self.geojson = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [16.00,50.00],
                        [16.10,50.10],
                        [16.20,50.20],
                        [16.30,50.30],
                        [16.00,50.00]
                    ]
                ]
            },
            "properties": {
                "name": "test_point"
            }
        }

    def test_here_catchment_as_geojson(self):
        geojson_feature = catchment_as_geojson(self.catchment, **self.params)
        self.assertEqual(geojson_feature, self.geojson)
    
    def test_here_catchment_name(self):
        geojson_feature = catchment_as_geojson(self.catchment, **self.params)
        self.assertEqual(geojson_feature['properties']['name'], self.geojson['properties']['name'])


class TestSaveAsGeojson(TestCase):

    def setUp(self):
        self.params = {'api': 'SKOBBLER', 'key': 'your_api_key'}
        # Create a temporary directory
        self.test_dir = mkdtemp()
        self.geojson = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [16.00,50.00],
                        [16.10,50.10],
                        [16.20,50.20],
                        [16.30,50.30],
                        [16.00,50.00]
                    ]
                ]
            },
            "properties": {
                "name": "test_point"
            }
        }

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

from unittest import TestCase
from unittest.mock import patch, Mock
from optparse import OptionParser
from io import StringIO
from catchments import create_parser, load_input_data, request_catchment, \
    catchment_as_geojson, save_as_geojson, validate_required_params
import csv
import requests


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
            self.assertEqual(row, csv.OrderedDict([('lat', '52.02'), ('lon', '16.02')]))
    

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


"""
# Run tests with:
# coverage run --branch --source=my_module/ setup.py test
# To check coverage report (with missing lines)
# coverage report -m

# Not functional for now
class TestSaveAsGeojson(TestCase):

    def setUp(self):
        self.params = {'api': 'SKOBBLER', 'key': 'your_api_key'}
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the directory after the test
        shutil.rmtree(self.test_dir)

    def test_save_as_geojson(self):
        pass
"""

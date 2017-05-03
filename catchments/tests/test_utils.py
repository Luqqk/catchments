from unittest import TestCase
from io import StringIO
from tempfile import mkdtemp
from shutil import rmtree
from catchments.utils import load_input_data
import csv
# csv.OrderedDict is supported only in Python > 3.6
# collections.OrderedDict for backward compatibility (Python < 3.6)
import collections


# Run tests with:
# coverage run --branch --source=catchments/ setup.py test
# To check coverage report (with missing lines)
# coverage report -m


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

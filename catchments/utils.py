import csv
from functools import wraps
from optparse import OptionParser


def create_parser():
    """Creates parser for commandline arguments.
    
    Returns:
        parser (optparse.OptionParser)
    """

    parser = OptionParser()
    
    # Required parameters
    parser.add_option(
        '-a', '--api', type='choice', choices=['HERE', 'SKOBBLER'],
        help='API provider (SKOBBLER, HERE)'
    )
    parser.add_option(
        '-k', '--key', type='string',
        help='SKOBBLER or HERE API key'
    )
    parser.add_option(
        '-p', '--points', type='string',
        help='*.csv file to read points from'
    )
    
    # Optional parameters
    parser.add_option(
        '-r', '--range', type='int', default=600,
        help='Range (int)'
    )
    parser.add_option('-u', '--units', type='choice',
        choices=['sec', 'meter', 'time', 'distance'], default='sec',
        help='Units (sec, meter, time, distance)'
    )
    parser.add_option('-t', '--transport', type='choice',
        choices=['pedestrian', 'bike', 'car'], default='car',
        help='Transport type (pedestrian, bike, car)'
    )
    parser.add_option(
        '-j', '--jam', type='choice',
        choices=['enabled', 'disabled'], default='enabled',
        help='Real time traffic (enabled, disabled)'
    )

    return parser


def load_input_data(points):
    """Creates DictReader from *.csv file.

    :param points (file object):
        *.csv file with
        'lon' (required),
        'lat' (required), 
        'name' (optional) columns.
    
    Returns:
        data (csv.DictReader)
    """

    dialect = csv.Sniffer().sniff(points.read())
    
    points.seek(0)

    data = csv.DictReader(points, dialect=dialect)
    
    return data

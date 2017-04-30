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
    parser.add_option(
        '-e', '--range-type', type='string', default='time',
        help='ONLY HERE. Range type (time, distance)'
    )
    parser.add_option(
        '-m', '--mode', type='string', default='fastest;car;traffic:disabled',
        help='''ONLY HERE. Mode - real time traffic and transport type
        (fastest;car;traffic:disabled)'''
    )
    parser.add_option(
        '-u', '--units', type='choice',
        choices=['sec', 'meter'], default='sec',
        help='ONLY SKOBBLER. Units (sec, meter)'
    )
    parser.add_option(
        '-t', '--transport', type='choice',
        choices=['pedestrian', 'bike', 'car'], default='car',
        help='ONLY SKOBBLER. (pedestrian, bike, car)'
    )
    parser.add_option(
        '-l', '--toll', type='choice',
        choices=['0', '1'], default='0',
        help='''ONLY SKOBBLER. Specifies whether to avoid or not 
        the use of toll roads in route calculation (0, 1)'''
    )
    parser.add_option(
        '-w', '--highways', type='choice',
        choices=['0', '1'], default='0',
        help='''ONLY SKOBBLER. Specifies whether to avoid or not
        the use of highways in route calculation (0, 1)'''
    )
    parser.add_option(
        '-n', '--non_reachable', type='choice',
        choices=['0', '1'], default='0',
        help='''ONLY SKOBBLER. Specifies whether to calculate
        or not the interior contours (non reachable areas)
        inside the RealReach™ (0, 1)'''
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

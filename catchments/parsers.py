from optparse import OptionParser


def create_skobbler_parser():
    """Creates parser for SKOBBLER commandline arguments.

    Returns:
        parser (optparse.OptionParser)
    """

    parser = OptionParser()
    
    # Required parameters
    parser.add_option(
        '-k', '--key', type='string',
        help='SKOBBLER API key'
    )
    parser.add_option(
        '-p', '--points', type='string',
        help='*.csv file to read points from'
    )
    
    # Optional parameters
    parser.add_option(
        '-r', '--range', type='string', default='600',
        help='Range (int)'
    )
    parser.add_option(
        '-u', '--units', type='choice',
        choices=['sec', 'meter'], default='sec',
        help='(sec, meter)'
    )
    parser.add_option(
        '-t', '--transport', type='choice',
        choices=['pedestrian', 'bike', 'car'], default='car',
        help='(pedestrian, bike, car)'
    )
    parser.add_option(
        '-l', '--toll', type='choice',
        choices=['0', '1'], default='0',
        help='''Specifies whether to avoid or not 
        the use of toll roads in route calculation (0, 1)'''
    )
    parser.add_option(
        '-w', '--highways', type='choice',
        choices=['0', '1'], default='0',
        help='''Specifies whether to avoid or not
        the use of highways in route calculation (0, 1)'''
    )
    parser.add_option(
        '-n', '--nonReachable', type='choice',
        choices=['0', '1'], default='0',
        help='''Specifies whether to calculate
        or not the interior contours (non reachable areas)
        inside the RealReach™ (0, 1)'''
    )

    return parser


def create_here_parser():
    """Creates parser for HERE commandline arguments.

    Returns:
        parser (optparse.OptionParser)
    """

    parser = OptionParser()
    
    # Required parameters
    parser.add_option(
        '-i', '--app_id', type='string',
        help='HERE API app_id'
    )
    parser.add_option(
        '-c', '--app_code', type='string',
        help='HERE API app_code'
    )
    parser.add_option(
        '-p', '--points', type='string',
        help='*.csv file to read points from'
    )
    
    # Optional parameters
    parser.add_option(
        '-r', '--range', type='string', default='600',
        help='Range (int)'
    )
    parser.add_option(
        '-t', '--rangetype', type='string', default='time',
        help='(time, distance)'
    )
    parser.add_option(
        '-m', '--mode', type='string', default='fastest;car;traffic:disabled',
        help='''Mode - real time traffic and transport type
        (fastest;car;traffic:disabled)'''
    )

    return parser

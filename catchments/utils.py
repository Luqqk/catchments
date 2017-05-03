import csv


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

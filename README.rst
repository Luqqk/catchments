Catchments
==========

Simple package for acquiring and manipulating catchments from SKOBBLER and HERE API.

Installation
------------

.. code-block:: bash

    $ pip install catchments

Usage
-----

You can use package functions to build Your own scripts:

.. code-block:: python

    >>> from catchments import request_catchment, catchment_as_geojson, \
            save_as_geojson

    >>> # get catchment from API
    >>> params = {'api': 'SKOBBLER', 'key': 'your_api_key'}
    >>> catchment = request_catchment({'lat' 50.0, 'lon': 19.0}, **params)
    >>> geojson = catchment_as_geojson(catchment, **params)
    >>> save_as_geojson(geojson, **params)
    >>> 'SKOBBLER_50.0_19.0.geojson'

Or You can use inbuilt command line script which accepts \*.csv file input with points as coordinates resource.

Example \*.csv file structure (name column is optional):

+------------+------------+-----------+ 
|    name    |    lat     |    lon    | 
+============+============+===========+ 
|   point1   | lat        | lon       | 
+------------+------------+-----------+ 
|   point2   | lat        | lon       | 
+------------+------------+-----------+ 

.. code-block:: bash

    $ catchments-cls.py -a SKOBBLER -k your_api_key -f path/to/*.csv

tbc...

Catchments
==========

Simple package for acquiring and manipulating catchments from SKOBBLER (Real Reach) and HERE (Isolines) API.

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
    >>> catchment = request_catchment({'lat' 52.05, 'lon': 16.82}, **params)
    >>> {"realReach": {...} ...}
    >>> geojson = catchment_as_geojson(catchment, **params)
    >>> {"type": "Feature", geometry: {"type": "Polygon", ...}, ...}
    >>> save_as_geojson(geojson, **params)
    >>> 'SKOBBLER_52.05_16.82.geojson'

Or You can use inbuilt command line script which accepts \*.csv file input with points as coordinates resource.

Example \*.csv file structure (name column is optional):

+------------+------------+------------+ 
|    name    |    lat     |    lon     | 
+============+============+============+ 
|   point1   |  52.0557   |  16.8278   | 
+------------+------------+------------+ 
|   point2   |  52.4639   |  16.9410   | 
+------------+------------+------------+ 

.. code-block:: bash

    $ catchments-cls.py -a SKOBBLER -k your_api_key -p path/to/file/with/points/*.csv

All supported options for command line script and package functions are mentioned below:

+-----------------+------------+---------------------------------------------------+ 
|    param        |required    |   default value                                   | 
+=================+============+===================================================+
|   api           |    Yes     |  **None**                                         | 
+-----------------+------------+---------------------------------------------------+ 
|   key           |    Yes     |  **None**                                         | 
+-----------------+------------+---------------------------------------------------+ 
|   points        |    Yes     |  **None** (required only by catchments-cls.py)    | 
+-----------------+------------+---------------------------------------------------+ 
|   range         |    No      |  **600**                                          | 
+-----------------+------------+---------------------------------------------------+ 
|   units         |    No      |  **sec** (SKOBBLER) **time** (HERE)               | 
+-----------------+------------+---------------------------------------------------+ 
|   transport     |    No      |  **car**                                          | 
+-----------------+------------+---------------------------------------------------+ 
|   jam           |    No      |  **disabled** (HERE API only)                     | 
+-----------------+------------+---------------------------------------------------+ 
|   toll          |    No      |  **1** (SKOBBLER API only)                        | 
|                 |            |  - currently not supported by catchments-cls.py   | 
+-----------------+------------+---------------------------------------------------+
|   highways      |    No      |  **1** (SKOBBLER API only)                        | 
|                 |            |  - currently not supported by catchments-cls.py   | 
+-----------------+------------+---------------------------------------------------+ 
|   non_reachable |    No      |  **1** (SKOBBLER API only)                        | 
|                 |            |  - currently not supported by catchments-cls.py   | 
+-----------------+------------+---------------------------------------------------+  

Tests
-----

.. code-block:: bash

    $ python setup.py test

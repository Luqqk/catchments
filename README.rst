.. image:: https://travis-ci.org/Luqqk/catchments.svg?branch=master
    :target: https://travis-ci.org/Luqqk/catchments

.. image:: https://coveralls.io/repos/github/Luqqk/catchments/badge.svg
    :target: https://coveralls.io/github/Luqqk/catchments

🌍 catchments
=============

Python wrapper for SKOBBLER RealReach and HERE Isolines API. It allows to acquire and manipulate catchments from those APIs.

Installation
------------

.. code-block:: bash

    $ pip install catchments

Usage
-----

.. code-block:: python

    >>> from catchments import SkobblerAPI, HereAPI

    >>> # get catchment from Skobbler API
    >>> skobbler = SkobblerAPI('your_api_key')
    >>> params = {"range": 600, "highways": 0}
    >>> catchment = skobbler.get_catchment({'lat' 52.05, 'lon': 16.82}, **params)
    >>> {"realReach": {...} ...}
    >>> geojson = skobbler.catchment_as_geojson(catchment)
    >>> {"type": "Feature", geometry: {"type": "Polygon", ...}, ...}
    >>> skobbler.save_as_geojson(geojson)
    >>> 'SKOBBLER_52.05_16.82.geojson'

Params supported by SKOBBLER and HERE:

`Skobbler RealReach API params <https://developer.skobbler.com/getting-started/web#sec3>`_

`HERE Isoline API params <https://developer.here.com/rest-apis/documentation/routing/topics/request-isoline.html>`_

Or You can use inbuilt command line script which accepts \*.csv file input with points as coordinates resource. It generates \*.geojson files for every point in given \*.csv file.

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

All supported options for command line script are mentioned below:

* api [required] - default value is **None**. You can choose from **SKOBBLER** and **HERE**

* key [required] - default value is **None**
    
    * SKOBBLER - "your_api_key"
    * HERE - "app_id,app_code"

* points [required] - default value is **None**. Path to \*.csv file with points.

* range - default value is:

    * SKOBBLER **600**
    * HERE **600**

* units - default value is:

    * SKOBBLER **sec**
    * HERE (rangetype) **time**

* transport - default value is:

    * SKOBBLER **car**
    * HERE **car**

* jam - default value is:

    * SKOBBLER not supported
    * HERE **disabled**

* toll - default value is (currently not supported by catchments-cls.py):

    * SKOBBLER 1
    * HERE not supported

* highways - default value is (currently not supported by catchments-cls.py):

    * SKOBBLER 1
    * HERE not supported

* non_reachable - default value is (currently not supported by catchments-cls.py):

    * SKOBBLER 1
    * HERE not supported

Tests
-----

.. code-block:: bash

    $ python setup.py test

TODO
------

* Add support for Mapzen API catchments

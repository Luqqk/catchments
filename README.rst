.. image:: https://travis-ci.org/Luqqk/catchments.svg?branch=master
    :target: https://travis-ci.org/Luqqk/catchments

.. image:: https://coveralls.io/repos/github/Luqqk/catchments/badge.svg
    :target: https://coveralls.io/github/Luqqk/catchments

🌍 catchments
=============

Python wrapper for SKOBBLER RealReach and HERE Isolines API. It allows to acquire and manipulate catchments from those APIs.

.. image:: img/catchments.png
    :scale: 50 %
    :target: https://github.com/Luqqk/catchments/blob/master/img/catchments.png

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
    >>> # if you don't provide params values default ones will be used
    >>> params = {"range": 600, "highways": 1}
    >>> catchment = skobbler.get_catchment({'lat' 52.05, 'lon': 16.82}, **params)
    >>> {"realReach": {...} ...}
    >>> geojson = skobbler.catchment_as_geojson(catchment)
    >>> {"type": "Feature", geometry: {"type": "Polygon", ...}, ...}
    >>> skobbler.save_as_geojson(geojson)
    >>> 'SKOBBLER_52.05_16.82.geojson'

Params supported by SKOBBLER and HERE:

`Skobbler RealReach API params <https://developer.skobbler.com/getting-started/web#sec3>`_ (startMercator, response_type - not supported)

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

* -a --api [REQUIRED] [SKOBBLER AND HERE] - default value is **None**. You can choose from **SKOBBLER** or **HERE**.

* -k --key [REQUIRED] [SKOBBLER AND HERE] - default value is **None**. Format this param like this:
    
    * SKOBBLER - "your_api_key"
    * HERE - "app_id,app_code"

* -p --points [REQUIRED] [SKOBBLER AND HERE] - default value is **None**:

    * SKOBBLER - path to \*.csv file with points
    * HERE - path to \*.csv file with points

* -r --range - [OPTIONAL] [SKOBBLER AND HERE] default value is:

    * SKOBBLER **600**
    * HERE **600**

* -e --range-type - [OPTIONAL] [HERE ONLY] default value is:

    * **time**

* -m --mode - [OPTIONAL] [HERE ONLY] default value is:

    * **fastest;car;traffic:disabled**

* -u --units - [OPTIONAL] [SKOBBLER ONLY] default value is:

    * **sec**

* -t --transport - [OPTIONAL] [SKOBBLER ONLY] default value is:

    * **car**

* -l --toll - [OPTIONAL] [SKOBBLER ONLY] default value is:

    * **0**

* -w --highways - [OPTIONAL] [SKOBBLER ONLY] default value is:

    * **0**

* -n --non_reachable - [OPTIONAL] [SKOBBLER ONLY] default value is:

    * **0**

Tests
-----

.. code-block:: bash

    $ python setup.py test

TODO
------

* Add support for Mapzen API catchments

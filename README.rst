.. image:: https://travis-ci.org/Luqqk/catchments.svg?branch=master
    :target: https://travis-ci.org/Luqqk/catchments

.. image:: https://coveralls.io/repos/github/Luqqk/catchments/badge.svg
    :target: https://coveralls.io/github/Luqqk/catchments

🌍 catchments
=============

Python wrapper for multiple APIs, that provide catchments-areas.
It allows to acquire and manipulate catchments from those APIs.
It can help you answer the questions like: "Where can I get in 30 min from that point?"
taking into account e.g. real traffic, transport type, specified range. 

.. image:: img/catchments.png
    :height: 400px
    :width: 400px
    :align: center
    :target: https://github.com/Luqqk/catchments/blob/master/img/catchments.png

Installation
------------

.. code-block:: bash

    $ pip install catchments

Usage
-----

Currently there are implemented two classes: **SkobblerAPI("api_key")** and **HereAPI("app_id", "app_code")**.

You can use them as follows:

.. code-block:: python

    >>> from catchments import SkobblerAPI

    >>> # get catchment from Skobbler API
    >>> skobbler = SkobblerAPI('your_api_key')
    >>> # if you don't provide params values default ones will be used
    >>> params = {"range": 600, "highways": 1}
    >>> catchment = skobbler.get_catchment({"lat": 52.40, "lon": 16.93}, **params)
    >>> {"realReach": {...} ...}
    >>> geojson = skobbler.catchment_as_geojson(catchment)
    >>> {"type": "Feature", geometry: {"type": "Polygon", ...}, ...}
    >>> skobbler.save_as_geojson(geojson)
    >>> 'SKOBBLER_52.40_16.93.geojson'

As you can see **.get_catchment** method uses **params** as second argument. Params keys names should be exactly the same
as mentioned in APIs documentations, otherwise they will be ignored and default values will be used.

Params supported by **SKOBBLER** and **HERE**:

`SKOBBLER <https://developer.skobbler.com/getting-started/web#sec3>`_ (startMercator, response_type - not supported)

`HERE <https://developer.here.com/rest-apis/documentation/routing/topics/request-isoline.html>`_

You can use also inbuilt command line scripts which accept \*.csv file input with points as coordinates resource.
Scripts generate \*.geojson files for every point in given \*.csv file.

Example \*.csv file structure (name column is optional):

+------------+------------+------------+ 
|    name    |    lat     |    lon     | 
+============+============+============+ 
|   point1   |  52.0557   |  16.8278   | 
+------------+------------+------------+ 
|   point2   |  52.4639   |  16.9410   | 
+------------+------------+------------+ 

Example command line script usage:

.. code-block:: bash

    $ catchments-skobbler.py -k your_api_key -p path/to/file/with/points/*.csv

All scripts and their options are mentioned below:

.. code-block:: bash

    $ catchments-skobbler.py

* -k --key [REQUIRED] [DEFAULT: **None**]

* -p --points [REQUIRED] [DEFAULT: **None**]

* -r --range - [OPTIONAL] [DEFAULT: **600**]

* -u --units - [OPTIONAL] [DEFAULT: **sec**]

* -t --transport - [OPTIONAL] [DEFAULT: **car**]

* -l --toll - [OPTIONAL] [DEFAULT: **0**]

* -w --highways - [OPTIONAL] [DEFAULT: **0**]

* -n --nonReachable - [OPTIONAL] [DEFAULT: **0**]

.. code-block:: bash

    $ catchments-here.py

* -i --app_id [REQUIRED] [DEFAULT: **None**]

* -c --app_code [REQUIRED] [DEFAULT: **None**]

* -r --range - [OPTIONAL] [DEFAULT: **600**]

* -e --range-type - [OPTIONAL] [DEFAULT: **time**]

* -m --mode - [OPTIONAL] [DEFAULT: **fastest;car;traffic:disabled**]

Tests
-----

.. code-block:: bash

    $ python setup.py test

TODO
----

* Add support for Mapzen API catchments
* Add support for OpenRouteService catchments
* Add support for concurrent HTTP requests

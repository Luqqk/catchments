EXAMPLE_SKOBBLER_PARAMS = {'api': 'SKOBBLER', 'key': 'your_api_key'}

EXAMPLE_HERE_PARAMS = {'api': 'HERE', 'key': 'your_app_id,your_app_code'}

EXAMPLE_SKOBBLER_CATCHMENT = {
    "realReach": {
        "gpsBBox": [10.00,45.00,16.00,52.00],
        "gpsPoints": [
            -180.0,85.051129,
            180.0,85.051129,
            180.0,-85.051129,
            -180.0,-85.051129,
            10.10,45.20,
            11.10,46.20,
            12.10,47.20,
            13.10,48.20,
            14.10,49.20,
            15.10,50.20
        ]
    },
    "name": "test_point"
}

EXAMPLE_HERE_CATCHMENT = {
    "response": {
        "isoline": [
            {"component": [
                    {"shape": [
                            "50.00,16.00",
                            "50.10,16.10",
                            "50.20,16.20",
                            "50.30,16.30",
                            "50.00,16.00",
                        ]
                    }
                ]
            }
        ]
    },
    "name": "test_point"
}

EXAMPLE_SKOBBLER_GEOJSON = {
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [10.10,45.20],
                [11.10,46.20],
                [12.10,47.20],
                [13.10,48.20],
                [14.10,49.20],
                [15.10,50.20],
                [10.10,45.20]
            ]
        ]
    },
    "properties": {
        "name": "test_point"
    }
}

EXAMPLE_HERE_GEOJSON = {
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [16.00,50.00],
                [16.10,50.10],
                [16.20,50.20],
                [16.30,50.30],
                [16.00,50.00]
            ]
        ]
    },
    "properties": {
        "name": "test_point"
    }
}

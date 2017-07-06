#!/usr/bin/env python

# if you want to access host through gateway.
# host and gateway must be a list
#
# following examples:
# ... 
# "idc-01": [host, gateway]
# ...
#
# Example
# group = {
#    "host": {
#       "idc-01": ["127.0.0.1","192.168.1.254"]
#    }
# ...
#}
#
# if dont need the gateway
# following example:
# ...
# "simu-01": "192.168.1.2"
# ...

simu_group = {
    "host": {
        "simu-01": "192.168.4.4",
        "simu-02": "192.168.1.25"
    },
    "port": {
        "gezi": 9100,
        "gbm": 5001
    },
    "url": {
        "gezi": [
            "curl -s -o /dev/null -w %{http_code} http://127.0.0.1:9100/test",
            "curl -s -o /dev/null -w %{http_code} http://127.0.0.1:9100/test"
        ],
        "gbm": [
            "curl -s -o /dev/null -w %{http_code} http://127.0.0.1:5001/test"
        ]
    }
}


idc_group = {
    "host": {
        "idc-01": ["127.0.0.1:1234","ubuntu@192.168.4.57"],
        "idc-02": ["127.0.0.1:1235","ubuntu@192.168.4.57"]
    },
    "port": {
        "gezi": 9100
    },
    "url": {
        "gezi": [
            "curl -s -o /dev/null -w %{http_code} http://127.0.0.1:9100/test"
        ]
    }
}

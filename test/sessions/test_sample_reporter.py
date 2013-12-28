import sys
sys.path.insert(0, "../../src")

import unittest
from sessions.http_sample_reporter import *
from common.fake_xig import FakeXigCore

class TestSampleReporter(unittest.TestCase):


    def test_null(self):
        xig = FakeXigCore()
        json_string = '{"__device": "weather", "__sample": {"__id":49, "Temp":null, ' \
                      '"RH":null, "AtmoPressure":1021.98, "AmbientLight":425, "BroadbandLight":1161, "Infrared":252}}'
        reporter = HttpSampleReporter.handleSessionCommand(xig, json_string, None)
        pass

    def test_get(self):
        xig = FakeXigCore()

        json_string = '{"__device": "weather", "__sample": {"__id":7, "Temp":20.40, ' \
                      '"RH":45.00, "AtmoPressure":1021.83, "AmbientLight":564, ' \
                      '"BroadbandLight":1575, "Infrared":361}}\n\n'
        reporter = HttpSampleReporter.handleSessionCommand(xig, json_string, None)
        pass


if __name__ == "__main__":
    unittest.main()


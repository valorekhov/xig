import sys
sys.path.insert(0, "../../src")

import unittest
from sessions.http_sample_reporter import *
from common.fake_xig import FakeXigCore

class TestSampleReporter(unittest.TestCase):

    def test_get(self):
        xig = FakeXigCore()

        json_string = '{"__device": "weather", "__sample": {"__id":25, "Temp":22.20, ' \
                    '"RH":49.40, "AtmoPressure":1027.01, "AmbientLight":97, ' \
                    '"BroadbandLight":3839, "Infrared":637}}'
        reporter = HttpSampleReporter.handleSessionCommand(xig, json_string, None)
        pass

if __name__ == "__main__":
    unittest.main()


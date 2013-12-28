import sys
sys.path.insert(0, "../../src")

from sessions.library import json
import unittest
from sessions.http_sample_reporter import *
from common.fake_xig import FakeXigCore

class TestSampleReporter(unittest.TestCase):
    def setUp(self):
        self.xig = FakeXigCore()

        data = json.read('{"_sensor": "weather", "_sample": {"_id":25, "Temp":22.20, '
                                                 '"RH":49.40, "AtmoPressure":1027.01, "AmbientLight":97, '
                                                 '"BroadbandLight":3839, "Infrared":637}}')

        #self.test_xbee = TestCaseBase.startTestXBee(self)
        self.reporter = HttpSampleReporter(self.xig, None, data["_sensor"], data["_sample"])
        pass

    def tearDown(self):
        #TestCaseBase.stopTestXBee(self)
        #TestCaseBase.stopXig(self)
        pass

    def test_get(self):
        #self.reporter.__connect()
        pass

if __name__ == "__main__":
    unittest.main()


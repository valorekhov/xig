from xig_config_test import XigConfig

__author__ = 'val'

class FakeXigCore(object):
    def __init__(self):
        self.config = XigConfig()

    def getConfig(self):
        return self.config

    def getShortName(self):
        return "XIG"

    def getVersion(self):
        return "999"

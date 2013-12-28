from sessions.library.json import ReadException

__author__ = 'val orekhov'
from sessions.library import json

class MessageFormatException(Exception):
    pass

class AbstractMessageFormat(object):
    def __init__(self, device, sample, command):
        self.device_name = device
        self.sample_dict = sample
        self.command_dict = command

    def is_sample(self):
        return self.sample_dict is not None

    def is_command(self):
        return self.command_dict is not None

    def device(self):
        return self.device_name

    def sample(self):
        return self.sample_dict

    def command(self):
        return self.command_dict

    @staticmethod
    def parse(string):
        string = str(string).strip()

        if string.startswith('{') and string.endswith('}') and ":" in string: #attempt to parse as JSON
            json = JsonMessage.parse(string)
            if json is not None:
                return json

        raise MessageFormatException, "Unsupported format for message: %s" % string


class JsonMessage(AbstractMessageFormat):
    def __init__(self, device, sample, command):
        super(JsonMessage, self).__init__(device, sample, command)

    @staticmethod
    def parse(string):
        data = None
        try:
         data = json.read(string)
        except ReadException:
            pass


        if data is not None:
             return JsonMessage(data["__device"], data.get("__sample"), data.get("__command"))

        return None


import httplib
import urllib
from messages.abstract_message import AbstractMessageFormat
import library.xig_urlparse as urlparse
import socket
import logging
from sessions.http import HTTPSession

logger = logging.getLogger("xig.httpsamplereporter")
logger.setLevel(logging.DEBUG)

from sessions.abstract import AbstractSession

import sys
if sys.version_info < (2, 5):
    # only needed with versions of Python < 2.5
    def all(iterable):
        for element in iterable:
            if not element:
                return False
        return True

class HttpSampleReporter(AbstractSession):
    
    def __init__(self, xig_core, xbee_addr, device, sample):
        self.__core = xig_core
        self.__write_buf = ""
        self.__read_buf = ""
        self.__xbee_addr = xbee_addr
        self.__max_buf_size = self.__core.getConfig().global_max_buf_size

        self.sensor = device
        self.sample = sample

        # Read configuration from configuration file:
        self.__targets = self.getTargetsFromConfig(device, sample)
        self.__connect()

    def parse_url(self, url):
        parsedurl = urlparse.urlsplit(url)

        scheme = parsedurl[0]
        authority = parsedurl[1]
        path = parsedurl[2]
        if len(parsedurl[3]):
            query =  + parsedurl[3]
        else:
            query = None

        return scheme, authority, path, query

    def concat_query_string(self, path, query, payload):
        if query is not None:
            path += '?' + query + '&'
        else:
            path += '?'
        path += urllib.urlencode(payload)
        return path

    def concat_post_body(self, path, query, payload):
        if query is not None:
            path += '?' + query
        postBody = urllib.urlencode(payload)
        return path, postBody

    def process_target(self, method, address, payload, ignore_response):
        scheme, authority, path, query = self.parse_url(address)

        if method == "GET":
            path = self.concat_query_string(path, query, payload)
            postBody = None
        elif method == "POST":
            path, postBody = self.concat_post_body(path, query, payload)

        url = "%s://%s%s" % (scheme, authority, path)

        if scheme == "https":
            # TODO: connect timeout
            self.__httpConn = httplib.HTTPSConnection(authority)
        else:
            # TODO: connect timeout
            self.__httpConn = httplib.HTTPConnection(authority)

        headers = {'Accept': 'text/plain, text/html',
                   'User-Agent': '%s-%s' % (self.__core.getShortName(),
                                            self.__core.getVersion())}
        try:
            self.__httpConn.request(method, path, postBody, headers)
            logger.info("successful %s of %s" % (method, url))
        except socket.gaierror, e:
            if not ignore_response:
                self.__do_error("unable to perform HTTP request '%s'" % str(e))
            else:
                self.__state = HTTPSession.STATE_FINISHED
            return False
        except socket.error, e:
            if not ignore_response:
                self.__do_error("unable to perform HTTP request '%s'" % str(e))
            else:
                self.__state = HTTPSession.STATE_FINISHED
            return False

        if ignore_response:
            self.close()
            self.__state = HTTPSession.STATE_FINISHED
            return True

        try:
            self.__httpResponse = self.__httpConn.getresponse()
        except socket.error, e:
            self.__do_error("error while parsing HTTP response: %s" % repr(str(e)))
            return False
        except Exception, e:
            self.__do_error("httplib exception: %s" % repr(str(e)))
            return False

        if self.__httpResponse.status in (300, 301, 302, 303):
            # redirect
            location = self.__httpResponse.msg.get('location').strip()
            if location:
                logger.info("redirect to %s" % (location))
                self.process_target("GET", location, payload, ignore_response)

        if self.__httpResponse.status != 200:
            logger.warning("status = %d, reason = %s" % (
                self.__httpResponse.status, self.__httpResponse.reason))

        if self.__httpConn.sock is None:
            # Since socket is closed, read on file object will not block:
            self.__write_buf += self.__httpResponse.read()
            if len(self.__write_buf) == 0:
                self.__state = HTTPSession.STATE_FINISHED
            else:
                self.__state = HTTPSession.STATE_DRAIN
            return True

        # configure socket for non-blocking I/O operation:
        self.__httpConn.sock.setblocking(0)
        self.__state = HTTPSession.STATE_CONNECTED

        if self.__httpResponse.length == 0:
            self.__do_error("0 length response from server")
            return False

        return True

    def process_targets(self, targets, ignore_response):
        for (method, address, payload) in targets:
            self.process_target(method, address, payload, ignore_response)

    def __connect(self, ignore_response=False):
        self.process_targets(self.__targets, ignore_response)

    def __do_error(self, error_msg):
        self.__write_buf = "Xig-Error: " + error_msg + "\r\n"
        #self.__multiclient.close()          # necessary?

    @staticmethod
    def get_config_section(config, sensorName):
        return getattr(config, "httpSampleReporter_" + sensorName, None)

    def getTargetsFromConfig(self, sensorName, sample):
        input_targets = HttpSampleReporter.get_config_section(self.__core.getConfig(), sensorName)
        targets = []
        if not isinstance(input_targets, list):
            x = input_targets
            input_targets = list()
            input_targets.append(x)
        for target in input_targets:
            target = dict(target)
            method = str(target["_method"]).upper()
            addr = target["_destination"]

            payload = dict()
            keys = sorted(key for key in target.keys() if not str(key).startswith("_"))
            for key in keys:
                value = str(target[key])
                if value.startswith("{") and value.endswith("}"):
                    live_field = value[1:-1]
                    if sample.has_key(live_field):
                        value = sample[live_field]
                payload[key] = value
            targets.append( (method, addr, payload) )

        return targets

    @staticmethod
    def handleSessionCommand(xig_core, cmd_str, xbee_addr):
        message = AbstractMessageFormat.parse(cmd_str)

        if message is not None and message.is_sample():
            device = message.device()
            section = HttpSampleReporter.get_config_section(xig_core.getConfig(), device)
            if section is not None:
                return HttpSampleReporter(xig_core, xbee_addr, device, message.sample())
        return None

    @staticmethod
    def commandHelpText():
        return """\
 send in json
"""

    
    def close(self):
       pass
    
    def isFinished(self):
        return True
    
    def getXBeeAddr(self):
        return self.__xbee_addr
    
    def getReadSockets(self):
        return []
    
    def getWriteSockets(self):
        return []
    
    def getSessionToXBeeBuffer(self):
        return self.__write_buf
    
    def getXBeeToSessionBuffer(self):
        return "" # stub to complete interface

    def appendSessionToXBeeBuffer(self, buf):
        self.__write_buf += buf # stub, not used
    
    def appendXBeeToSessionBuffer(self, buf):
        self.__read_buf += buf
        self.__read_buf = self.__read_buf.replace("\r", "\n")
        self.__read_buf = self.__read_buf.replace("\n\n", "\n")
        if self.__read_buf.find("abort\n") > -1:
            self.close()
            self.__read_buf = ""
        elif len(self.__read_buf) > self.__max_buf_size:
            sidx = len(self.__read_buf) - self.__max_buf_size
            self.__read_buf = self.__read_buf[sidx:]
        
    def accountSessionToXBeeBuffer(self, count):
        self.__write_buf = self.__write_buf[count:]

    def read(self, sd):
        return 0
        
    def write(self, sd):
        return 0 # stub, this should never be called


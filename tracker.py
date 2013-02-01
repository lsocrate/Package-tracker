import httplib
import pprint
from HTMLParser import HTMLParser

class SROParser(HTMLParser):
    def __init__(self):
        super(SROParser, self).__init__()
        self.recording = 0
        self.data = []

    def handle_starttag(self, tag, attributes):
        if tag != "table":
            return
        if self.recording:
            self.recording += 1
            return
        for name, value in attributes:
            if name == "tr":
                print value


class Package(object):
    """Package to be tracked"""

    def __init__(self):
        super(Package, self).__init__()
        self.post_ofice_domain = "websro.correios.com.br"
        self.post_ofice_base_path = "/sro_bin/txect01$.QueryList?P_LINGUA=001&P_TIPO=001&P_COD_UNI="

    def set_track_code(self, track_code):
        self.track_code = track_code
        return self

    def request_package_track(self):
        connection = httplib.HTTPConnection(self.post_ofice_domain)
        connection.request("GET", self.post_ofice_base_path + self.track_code)
        response = connection.getresponse()

        return response.read()

    def get_package_track(self):
        html = self.request_package_track()
        parser = SROParser()
        parser.feed(html)
        parser.close()


pack = Package()
pack.set_track_code("CW258710596US")

print pack.get_package_track()
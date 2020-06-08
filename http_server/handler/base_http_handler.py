from util import date_time_string
from handler.base_handler import StreamRequestHandler
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

class BaseHTTPRequestHandler(StreamRequestHandler):

    def __init__(self, server, request, client_address):
        self.request_line = None
        self.method = None
        self.path = None
        self.version = None
        self.headers = None
        self.body = None
        StreamRequestHandler.__init__(self, server, request, client_address)

    #handle the request
    def handle(self):
        try:
            #1.parse request
            if not self.parse_request():
                return
            #2.do method(GET POST)
            method_name = 'do_' + self.method
            #3.whether or not a method exists
            if not hasattr(self, method_name):
                self.write_err(404, None)
                self.send()
                return
            method = getattr(self, method_name)
            method() #response
            #send result
            self.send()
        except Exception as e:
            logging.exception(e)

    def do_GET(self):
        msg = '<h1>Hello World</h1>'
        self.write_response(200, 'Success')
        self.write_header('Content-Length', len(msg))
        self.end_headers()
        self.write_content(msg)
        pass

    def parse_headers(self):
        headers = {}
        while True:
            line = self.readline()
            if line:
                key, value = line.split(",",1)
                key = key.strip()
                value = value.strip()
                headers[key] = value
            else:
                break
        return headers

    #parse the request
    def parse_request(self):
        #parse the request-line
        first_line = self.readline()
        self.request_line = first_line
        words = first_line.split()
        # method path and HEEP version from the request line
        self.method, self.path, self.version = words

        #parse the request-head
        self.headers = self.parse_headers()

        #parse the request-content
        key = 'Content-Length'
        if key in self.headers.keys():
            #length of the request content
            body_length = int(self.headers[key])
            self.body = self.read(body_length)
        return True

    def write_header(self, key, value):
        msg = '%s: %s\r\n' % (key, value)
        self.write_content(msg)

    default_http_version = 'Http/1.1'

    def write_response(self, code, msg=None):
        logging.info("%s, code,: %s." % (self.request_line, code))
        #response-line
        response_line = '%s %d %s\r\n' % (self.default_http_version, code, msg)
        self.write_content(response_line)
        #response-header
        self.write_header('Server', '%s: %s' % (self.server.server_name, self.server.version))
        self.write_header('Date', date_time_string())

    DEFAULT_ERROR_MESSAGE_TEMPLATE = r'''
        <head>
        <title>Error response</title>
        </head>
        <body>
        <h1>Error response</h1>
        <p>Error code %(code)d.
        <p>Message: %(message)s.
        <p>Error code explanation: %(code)s = %(explain)s.
        </body>
        '''

    responses = {
        100: ('Continue', 'Request received, please continue'),
        101: ('Switching Protocols',
              'Switching to new protocol; obey Upgrade header'),

        200: ('OK', 'Request fulfilled, document follows'),
        201: ('Created', 'Document created, URL follows'),
        202: ('Accepted',
              'Request accepted, processing continues off-line'),
        203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
        204: ('No Content', 'Request fulfilled, nothing follows'),
        205: ('Reset Content', 'Clear input form for further input.'),
        206: ('Partial Content', 'Partial content follows.'),

        300: ('Multiple Choices',
              'Object has several resources -- see URI list'),
        301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
        302: ('Found', 'Object moved temporarily -- see URI list'),
        303: ('See Other', 'Object moved -- see Method and URL list'),
        304: ('Not Modified',
              'Document has not changed since given time'),
        305: ('Use Proxy',
              'You must use proxy specified in Location to access this '
              'resource.'),
        307: ('Temporary Redirect',
              'Object moved temporarily -- see URI list'),

        400: ('Bad Request',
              'Bad request syntax or unsupported method'),
        401: ('Unauthorized',
              'No permission -- see authorization schemes'),
        402: ('Payment Required',
              'No payment -- see charging schemes'),
        403: ('Forbidden',
              'Request forbidden -- authorization will not help'),
        404: ('Not Found', 'Nothing matches the given URI'),
        405: ('Method Not Allowed',
              'Specified method is invalid for this resource.'),
        406: ('Not Acceptable', 'URI not available in preferred format.'),
        407: ('Proxy Authentication Required', 'You must authenticate with '
                                               'this proxy before proceeding.'),
        408: ('Request Timeout', 'Request timed out; try again later.'),
        409: ('Conflict', 'Request conflict.'),
        410: ('Gone',
              'URI no longer exists and has been permanently removed.'),
        411: ('Length Required', 'Client must specify Content-Length.'),
        412: ('Precondition Failed', 'Precondition in headers is false.'),
        413: ('Request Entity Too Large', 'Entity is too large.'),
        414: ('Request-URI Too Long', 'URI is too long.'),
        415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
        416: ('Requested Range Not Satisfiable',
              'Cannot satisfy request range.'),
        417: ('Expectation Failed',
              'Expect condition could not be satisfied.'),

        500: ('Internal Server Error', 'Server got itself in trouble'),
        501: ('Not Implemented',
              'Server does not support this operation'),
        502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
        503: ('Service Unavailable',
              'The server cannot process the request due to a high load'),
        504: ('Gateway Timeout',
              'The gateway server did not receive a timely response'),
        505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
    }

    def write_err(self, code, msg=None):
        s_msg, l_msg = self.responses[code]
        if msg:
            s_msg = msg
        response_content = self.DEFAULT_ERROR_MESSAGE_TEMPLATE % {
            'code': code,
            'message': s_msg,
            'explain': l_msg
        }
        self.write_response(code, s_msg)
        #there should be a space line between the response-header and response-line
        self.end_headers()
        self.write_content(response_content)

    def end_headers(self):
        self.write_content('\r\n')
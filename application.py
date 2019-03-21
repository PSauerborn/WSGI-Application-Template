

import cgi
import time

# the following code implements a simple REST interface using the WSGI standard specifications. Note that al functions (including the main applciation method) must take two arguments (the environ dictionary and the start_response function object).

def notfound_404(environ, start_response):
    """Function that is called by default when the request made does not match any registered function"""

    start_response('404 Not Found', [('Content-type', 'text/plain')])
    return [b'Not Found']

class PathDispatcher():
    """Application that implements WSGI specifications to handle requests"""

    def __init__(self):

        # the pathmap dictionary contains the registered functions that are called when a request is made. Note that the keys are tuples of form (request_method, path)

        self.pathmap = {}

    def __call__(self, environ, start_response):
        """ Method that is called when a request is made. Note that the __call__ function must be implemenetd for the application to work

        Parameters
        ----------
        environ: dict
            dictionary containing CGI like variables detailing the parameters of any request made
        start_response: function object
            callback function that is used by the application itself to send HTTP rquests and status Codes to the underlying server

        Returns
        -------

        handler: function object
            function that returns the actual data requested. Note the calling signature function(environ, start_response)


        """

        # the path/resource requested is first extracted. Note that the path along with the request method form the keys that determine which function is called to handle the request

        path = environ['PATH_INFO']

        # query parameters are extraced using the FieldStorage function from the cgi module. The FieldStorage function stores the values in a dictionary for later use

        params = cgi.FieldStorage(environ['wsgi.input'], environ=environ)

        # the request method is then extracted. Note that request method forms part of the key used for retrieving the correct handle method

        method = environ['REQUEST_METHOD'].lower()

        # parameters extracted using the cgi.FieldStorage function are then stored in the original environ dictionary in a slightly different format. This can be done at function level as well, if desired

        environ['params'] = {key: params.getvalue(key) for key in params}

        # the specified handeling method is then callled. Note that the get() function is used and, if the request tries to call a handler function not specified, the notfound_404 function defined above is returned instead

        handler = self.pathmap.get((method, path), notfound_404)

        # the handler function

        return handler(environ, start_response)

    def register(self, method, path, function):
        """Method used to register functions

        Parameters
        ----------
        environ: dicitonary
            dictionary containing values provided by web server
        method: str
            request method i.e. GET, POST etc
        path: str
            url path
        function: function object
            function to handle request

        """

        self.pathmap[method.lower(), path] = function
        return function

# in order to use the above, one simply has to define a set of handlers. These consist of a function and some data from (HTML JSON or XML). An example of this is given below

_hello_resp = """\

<html>
    <head>
        <title>Hello {name} {last} </title
    </head>
    <div>
    <body>
        <h1>Hello {name} {last}</h1>
    </body>
    </div>
    <div>
        <h1>How are you Today?</h1>
    </div>
</html>
"""

def hello_world(environ, start_response):
    """Function that handles a hello_world request by simple returning HTML data that displays a Hello World like message"""

    # the start_response must be called in order to initiate a response. The first argument is the HTTP status. The second value is a list of (name, value) tuples that make up the HTTP headers of the response. Note that any values returned MUST be of
    # byte-string format

    start_response('200 OK', [('Content-type', 'text/html')])
    params = environ['params']

    # the HelloWorld string is formatted with the given parameters

    resp = _hello_resp.format(name=params.get('name'), last=params.get('last', None))

    yield resp.encode('utf-8')

_localtime_resp = """/

<?xml version="1.0"?>
<time>
    <year>{t.tm_year}</year>
    <month>{t.tm_mon}</month>
    <day>{t.tm_mday}</day>
    <hour>{t.tm_hour}</hour>
    <minute>{t.tm_min}</minute>
    <second>{t.tm_sec}</second>
"""

def local_time(environ, start_response):
    start_response('200 OK', [('Content-type', 'application/xml')])
    resp = _localtime_resp.format(t=time.localtime())
    yield resp.encode('utf-8')

# the application is then run as follows

if __name__ == "__main__":

    from wsgiref.simple_server import make_server

    # the server is made and the functions are registed with it

    dispatcher = PathDispatcher()
    dispatcher.register('GET', '/hello', hello_world)
    dispatcher.register('GET', '/localtime', local_time)

    httpd = make_server('', 8080, dispatcher)
    print('Serving on port 8080')


    httpd.serve_forever()

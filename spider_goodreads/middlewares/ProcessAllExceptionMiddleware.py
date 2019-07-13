from scrapy.http import HtmlResponse
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError


class ProcessAllExceptionMiddleware(object):
    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                      ConnectionRefusedError, ConnectionDone, ConnectError,
                      ConnectionLost, TCPTimedOutError, ResponseFailed,
                      IOError, TunnelError)

    def process_response(self, request, response, spider):
        if str(response.status).startswith('4') or str(response.status).startswith('5'):
            response = HtmlResponse(url='')
            return response
        return response

    def process_exception(self, request, exception, spider):

        if isinstance(exception, self.ALL_EXCEPTIONS):

            print('Got exception: %s' % (exception))

            response = HtmlResponse(url='exception')
            return response

        print('not contained exception: %s' % exception)
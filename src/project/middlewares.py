import json

# DJANGO LIBRARY IMPORT
from django.http import HttpResponse


class ExceptionsMiddleware(object):
    """ A middleware for handling exceptions """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):

        response = {'error': exception.__class__.__name__ + ': ' + str(exception)}

        return HttpResponse(json.dumps(response, ensure_ascii=False),
                            status=400)

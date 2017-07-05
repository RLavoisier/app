from django.http import JsonResponse
import json

"""
        Helper class for REST API Json response
"""

class HJsonResponse():

    def __init__(self):
        self.response = {}
    """
        Return a Json formated response
    """
    def getResponse(self, error, message, data):
        self.response = {
            'error'     : error,
            'message'   : message,
            'data'      : data
        }
        return JsonResponse(self.response, safe=False)

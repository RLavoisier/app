from django.http import JsonResponse
import json

"""
        Helper class for REST API Json response
"""

class HJsonResponse():

    def __init__(self):
        self.jsonResponse           = {}
        self.jsonResponse.error     = False
        self.jsonResponse.message   = ""
        self.jsonResponse.data      = None


    """
        Return a Json formated response
    """
    def getResponse(self, error, message, data):
        self.jsonResponse.error     = error
        self.jsonResponse.message   = message
        self.jsonResponse.data      = data

        return json.dumps(self.jsonResponse)

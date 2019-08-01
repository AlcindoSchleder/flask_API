# -*- coding: utf-8 -*-
from common.helpers.errorCodes import ErrorCodes
from common.helpers import defaultObject

""" 
    class       : OperationResults
    descritption: Class to normalize messages to app 
    author      : Alcindo Schleder
    version     : 1.0.0
    package     : i-City Identification Plataform
"""
class OperationResults(ErrorCodes):
    def __init__(self, *args, **kwargs):
        super(OperationResults, self).__init__()
        self._result = defaultObject

    def _validateDictionary(self, value: dict = None):
        return bool((value.get("data")) and 
            (value.get("state")) and 
            (value["state"].get("sttCode")) and 
            (value["state"].get("sttMsgs")))

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value: dict = None):
        if ((value) and (self._validateDictionary(value))):
            self._result = value
        else:
            self._result = defaultObject

    @property
    def resultStatusCode(self):
        return self._result['state']['sttCode']

    @resultStatusCode.setter
    def resultStatusCode(self, sttCode: int):
        self._result['state']['sttCode'] = sttCode
        self._result['state']['sttMsgs'] = self.errorCodeDescr(sttCode)

    @property
    def resultData(self):
        return self._result["data"]

    @resultData.setter
    def resultData(self, value):
        self._result["data"] = value

    @property
    def resultStatusMessage(self):
        return self._result["state"]["sttMsgs"]

    @resultStatusMessage.setter
    def resultStatusMessage(self, message: str):
        self._result['state']['sttMsgs'] = message
        if (self._result['state']['sttCode'] == 200):
            self._result['state']['sttCode'] = self.getErrorCodeFromDescr(message)

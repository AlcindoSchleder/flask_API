# -*- coding: utf-8 -*-
from common import COMMON_DIRECTORY
from common.helpers.loadConfig import LoadJsonFiles

"""
    Class that inform a error code of http list
    * class      httpErrorCodes
    * requires   python 3.+, PyQt5
    * version    1.0.0
    * package    pyCommom
    * subpackage pyCommom
    * author     Alcindo Schleder <alcindoschleder@gmail.com>
    * copyright  Vocatio Telecom <https://www.vocatiotelecom.com.br>
"""
class ErrorCodes:

    ERROR_FILENAME = f'{COMMON_DIRECTORY}/httpErrorCodes.json'
    
    def __init__(self):
        conf = LoadJsonFiles(self.ERROR_FILENAME) 
        self._errorCodesList = dict(conf.dictData)

    @property
    def errorList(self):
        return self._errorCodesList

    @property
    def errorGroup(self, code: int = 200):
        grp = self._isValid(code)
        if (grp):
            return self._errorCodesList[grp]["code"]
        else:
            raise NotImplementedError(404)
    
    @property
    def errorGroupAndCodeDescr(self, code: int = 200):
        grp = self._isValid(code)
        if (grp):
            return { 
                "groupName": self._errorCodesList[grp]["name"],
                "codeDescr": self._errorCodesList[grp]["code"][code]
            }
        else:
            raise NotImplementedError(404)

    def _isValid(self, code: int = 200):
        grp = str(code)
        strCode = grp
        if (code < 99):
            grp = '4'
        grp = grp[0] + 'xx'
        if ((self._errorCodesList.get(grp)) and 
            (self._errorCodesList[grp].get("code")) and 
            (self._errorCodesList[grp]["code"].get(strCode))):
            return grp, strCode
        else:
            return False, False
    
    def errorCodeDescr(self, code: int = 200):
        grp, strCode = self._isValid(code)
        if (grp):
            strMsgs = self._errorCodesList[grp]["code"][strCode]
            return strMsgs
        else:
            raise NotImplementedError(404)
    
    def inspectDictData(self, data: dict, descr: str, level: int = 1):
        for key, value in data.items():
            if (value == descr):
                return key, value
            if (type(value) == dict):
                level += 1
                key, value = self.inspectDictData(value, descr, level)
                level -= 1
                if (value == descr): break
        return key, value

    def getErrorCodeFromDescr(self, description: str):
        result = self.inspectDictData(self, self._errorCodesList, description)
        return result[1]

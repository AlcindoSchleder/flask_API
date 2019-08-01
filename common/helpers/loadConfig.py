# -*- coding: utf-8 -*-
import configparser
import json
import os  
import hashlib
from common.helpers import defaultObject

""" 
    class       : LoadJsonFiles
    descritption: Class that load a json file and transform in a dict to return 
    author      : Alcindo Schleder
    version     : 1.0.0
    package     : i-City Identification Plataform
"""
class LoadJsonFiles: 
 
    def __init__(self, fileName: str, dataConfig: str = None):
        self._fn = None
        self._dataConfig = dataConfig
        if (self._checkFile(fileName)):
            self._fn = fileName
        else:
            raise Exception(f"File {fileName} not found!")
        
        self._jsonFileConfig = {}
        try:
            if (self._fn):
                with open(self._fn, 'r') as f:
                    self._jsonFileConfig = json.load(f)
                    f.close()
        except Exception as e:
            self._jsonFileConfig = {}
            raise Exception(e.args)

    def _checkFile(self, filename: str):
        return os.path.isfile(filename)

    def _generate_hash(self):
        BLOCKSIZE = 65536
        hasher = hashlib.sha256()
        with open(self._fn, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        return hasher

    def checkFileHash(self, config_filehash: str):
        retObj = defaultObject
        if (not self._checkFile(self._fn)):
            retObj['state']['sttCode'] = 401
            retObj['state']['sttMsgs'] = 'Erro: Arquivo de configuração não existe!'
            return retObj
        hasher = self._generate_hash()
        if (config_filehash != hasher.hexdigest()):
            retObj['state']['sttCode'] = 401
            retObj['state']['sttMsgs'] = 'Erro: Arquivo de configuração foi comprometido!'
        return retObj

    @property
    def dictData(self):
        if (self._dataConfig):
            return dict(self._jsonFileConfig[self._dataConfig])
        else:
            return dict(self._jsonFileConfig)

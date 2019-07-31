# -*- coding: utf-8 -*-
import hmac
import hashlib
import base64

""" 
    unit        : utils
    descritption: Collection of functions used in all projetcts
    author      : Alcindo Schleder
    version     : 1.0.0
    package     : i-City Identification Plataform
"""
def isnumber(value):
    try:
        float(value)
    except ValueError:
        return False
    return True

def calcFileSignature(data: str, password: str = None):
    if (password):
        digest  = hmac.new(password, msg=data, digestmod=hashlib.sha256).digest()
        resHash = base64.b64encode(digest).decode()
    else:
        hasher = hashlib.sha256()
        hasher.update(data)
        resHash = hasher.hexdigest()
    return resHash


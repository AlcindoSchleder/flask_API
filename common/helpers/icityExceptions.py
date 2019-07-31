""" 
    class       : UserNotHasPermission
    descritption: Exception for users that not has permissions
    author      : Alcindo Schleder
    version     : 1.0.0
    package     : i-City Identification Plataform
"""
class UserNotHasPermission(Exception):
    def __init__(self, aPermissionName):
        _msg = "User has not permission to execute %s db operation!" % (aPermissionName)
        super(UserNotHasPermission, self).__init__(_msg)

""" 
    class       : InvalidPermissionException
    descritption: Exception for users that not has permissions
    author      : Alcindo Schleder
    version     : 1.0.0
    package     : i-City Identification Plataform
"""
class InvalidPermissionException(Exception):
    def __init__(self, aPermission: int = 0):
        _msg = "Attempting to assign an invalid user permission(%d)!" % (aPermission)
        super(InvalidPermissionException, self).__init__(_msg)

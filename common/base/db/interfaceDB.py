import common.helpers.icityExceptions as ictyError
from common.helpers.operationResults import OperationResults

""" 
    vars        : Constants Definitions
    descritption: Constants defintion for Users Permitions
    author      : Alcindo Schleder
    version     : 1.0.0
    package     : i-City Identification Plataform
"""
FLAG_BROWSE = 0x0001
FLAG_INSERT = 0x0002
FLAG_UPDATE = 0x0004
FLAG_DELETE = 0x0008

ADMIN_PERM  = (FLAG_BROWSE & FLAG_INSERT & FLAG_UPDATE & FLAG_DELETE)
CLIENT_PERM = (FLAG_BROWSE & FLAG_INSERT & FLAG_UPDATE)
WRITE_PERM  = (FLAG_BROWSE & FLAG_INSERT)
UPDATE_PERM = (FLAG_BROWSE & FLAG_UPDATE)
READ_PERM   = FLAG_BROWSE

DSC_PERM = { 
    FLAG_BROWSE: 'Read',
    FLAG_INSERT: 'Insert',
    FLAG_UPDATE: 'Edit',
    FLAG_DELETE: 'Delete',
    ADMIN_PERM : 'Administrator',
    CLIENT_PERM: 'Client'
}

""" 
    class       : DBOperations
    descritption: Basic CRUD Operations for to Determine User Permissions
    author      : Alcindo Schleder
    version     : 1.0.0
    package     : i-City Identification Plataform
"""
class DBOperations():

    def __init__(self):
        pass

    def getValidPermissions(self):
        return [
            ADMIN_PERM, 
            CLIENT_PERM, 
            WRITE_PERM, 
            UPDATE_PERM,
            READ_PERM
        ]


""" 
    class       : IDatabases
    descritption: Basic CRUD Database class to use as Interface 
    author      : Alcindo Schleder
    version     : 1.0.0
    package     : i-City Identification Plataform
"""
class IDatabases(OperationResults, DBOperations):

    def __init__(self):
        super(IDatabases, self).__init__()
        self._validPermissions = self.getValidPermissions()
        self._userPermission   = READ_PERM
        self._db = None

    def _canExec(self, aPermission):
        return (self._userPermission & aPermission)

    def _config_db(self):
        raise NotImplementedError()

    def _connect(self):
        raise NotImplementedError()

    def browseRecord(self, item, skip, limit):
        if (not self._canExec(FLAG_BROWSE)):
            raise ictyError.UserNotHasPermission(DSC_PERM[FLAG_BROWSE])
        raise NotImplementedError()

    def insertRecord(self, item):
        if (not self._canExec(FLAG_INSERT)):
            raise ictyError.UserNotHasPermission(DSC_PERM[FLAG_INSERT])
        raise NotImplementedError()
        
    def updateRecord(self, aWhere, item):
        if (not self._canExec(FLAG_UPDATE)):
            raise ictyError.UserNotHasPermission(DSC_PERM[FLAG_UPDATE])
        raise NotImplementedError()

    def deleteRecord(self, aWhere):
        if (not self._canExec(FLAG_DELETE)):
            raise ictyError.UserNotHasPermission(DSC_PERM[FLAG_DELETE])
        raise NotImplementedError()

    def isConnected(self):
        raise NotImplementedError()

    def setPermission(self, aNewPermission: int = READ_PERM):
        if (not (aNewPermission in self._validPermissions)):
            raise ictyError.InvalidPermissionException(aNewPermission)
        self._userPermission = aNewPermission


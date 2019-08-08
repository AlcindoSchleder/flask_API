# -*- coding: utf-8 -*-
from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declared_attr, as_declarative

"""
    Base Class to init all schema classes
    * class      SchemaBase
    * requires   python 3.5+
    * version    1.0.0
    * package    icity-BlockChain
    * author     Alcindo Schleder <alcindoschleder@gmail.com>
    * copyright  Vocatio Telecom <https://www.vocatiotelecom.com.br>
"""
@as_declarative()
class SchemaBase:

    __name__ = None

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    def _asdict(self):
        return {c.key: getattr(self, c.key)
            for c in inspect(self).mapper.column_attrs}

    def __repr__(self):
        s = f'<{self.__tablename__}('
        for c in inspect(self).mapper.column_attrs:
            s += f'{c.key}={getattr(self, c.key)}, '
        s = s[:len(s) - 2] + ')>'
        return s

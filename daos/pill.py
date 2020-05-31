from daos import consts
import pyodbc


class PillDAO:
    def __init__(self):
        self.__conn = pyodbc.connect(f'DRIVER={consts.DRIVER};'
                                     f'SERVER={consts.SERVER};'
                                     f'DATABASE={consts.DATABASE};'
                                     f'UID={consts.USERNAME};'
                                     f'PWD={consts.PASSWORD};'
                                     f'Trusted_Connection=yes;')

        self.__cursor = self.__conn.cursor()

    def get(self, query_key, **kwargs):
        self.__cursor.execute(consts.QUERIES[query_key].format(kwargs["format"]))
        columns_names = [desc[0] for desc in self.__cursor.description]
        return self.__cursor.fetchall(), columns_names

    def update(self, query_key, **kwargs):
        self.__cursor.execute(consts.QUERIES[query_key].format(*kwargs["format"]))
        self.__conn.commit()

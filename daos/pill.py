from daos import consts
import pymssql


class PillDAO:
    def __init__(self):
        self.__conn = pymssql.connect(server=consts.SERVER,
                                      user=consts.USERNAME,
                                      password=consts.PASSWORD,
                                      database=consts.DATABASE)

        self.__cursor = self.__conn.cursor()

    def get(self, query_key: str):
        self.__cursor.execute(consts.QUERIES[query_key])
        return self.__cursor.fetchall()

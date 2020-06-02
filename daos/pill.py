from daos import consts
import pyodbc  # library for working with sql server


class PillDAO:
    def __init__(self):
        self.__conn = pyodbc.connect(f'DRIVER={consts.DRIVER};'
                                     f'SERVER={consts.SERVER};'
                                     f'DATABASE={consts.DATABASE};'
                                     f'UID={consts.USERNAME};'
                                     f'PWD={consts.PASSWORD};'
                                     f'Trusted_Connection=yes;')  # connection to the database

        self.__cursor = self.__conn.cursor()  # enable query execute

    def get(self, query_key, **kwargs):  # get data from database with optional parameters (WHERE {})
        self.__cursor.execute(consts.QUERIES[query_key].format(kwargs["format"]))  # running the query
        columns_names = [desc[0] for desc in self.__cursor.description]  # extract columns names from result
        return self.__cursor.fetchall(), columns_names  # return row values with columns names

    def update(self, query_key, **kwargs):  # update the is_obtained column in Collect to true/false
        self.__cursor.execute(consts.QUERIES[query_key].format(*kwargs["format"]))  # run update query with inserted data.
        self.__conn.commit()  # update the database table

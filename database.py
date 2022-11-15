import cx_Oracle
from psycopg2.pool import ThreadedConnectionPool
from functools import lru_cache
from helper import get_var_env


class DatabasePG:
    def __init__(self, database: str = get_var_env('PGDATABASE', ''), host: str = get_var_env('PGHOST', ''), password: str = get_var_env('PGPASSWORD', ''), user: str = get_var_env('PGUSER', ''), port: str = get_var_env('PGPORT', '')):
        self.__database = database
        self.__host = host
        self.__password = password
        self.__user = user
        self.__port = port
        self.__pool_conn = self.__create_connection()

    def __create_connection(self):
        try:
            pool_connection = ThreadedConnectionPool(
                minconn=1,
                maxconn=2,
                dsn=f'postgresql://{self.__user}:{self.__password}@{self.__host}:{self.__port}/{self.__database}?application_name=python-postgresql-conn'
            )
            return pool_connection
        except Exception as e:
            raise ValueError(e)

    def get_pool_conn(self):
        return self.__pool_conn.getconn()

    def put_pool_conn(self, conn):
        return self.__pool_conn.putconn(conn)

    def close_coon(self):
        self.__pool_conn.closeall()

class DatabaseORA:
    def __init__(self, database: str = get_var_env('ORADATABASE', ''), host: str = get_var_env('ORAHOST', ''), password: str = get_var_env('ORAPASSWORD', ''), user: str = get_var_env('ORAUSER', ''), port: str = get_var_env('ORAPORT', '')):
        self.__database = database
        self.__host = host
        self.__password = password
        self.__user = user
        self.__port = port
        self.__conn = self.__create_connection()

    def __create_connection(self):
        try:
            dsn_tns = cx_Oracle.makedsn(self.__host, self.__port, service_name=self.__database)
            conn = cx_Oracle.connect(user=self.__user, password=self.__password, dsn=dsn_tns)
            return conn
        except Exception as e:
            raise ValueError(e)

    def get_conn(self):
        return self.__conn


database_pg_obj = DatabasePG()

database_ora_obj = DatabaseORA()


@lru_cache
def get_connection_pg() -> DatabasePG:
    return database_pg_obj

@lru_cache
def get_connection_ora() -> DatabaseORA:
    return database_ora_obj

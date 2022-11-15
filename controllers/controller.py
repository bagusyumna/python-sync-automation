import logging
from database import get_connection_pg
from repositories.repositoryPostgresql import RepositoryPostgresql
from repositories.repositoryOracle import RepositoryOracle
from helper import get_var_env


class ControllerSync:
    def __init__(self):
        self.__conn = get_connection_pg()
        self.__chunk_size = int(get_var_env('CHUNKSIZE', 100))

    def __get_conn(self):
        return self.__conn.get_pool_conn()

    def __put_conn(self, pool):
        self.__conn.put_pool_conn(pool)

    def __close_conn(self):
        self.__conn.close_coon()

    def sync_karyawan(self):
        database_repo_oracle = RepositoryOracle()
        data = database_repo_oracle.get_all_data()

        logging.info(f"===================== sync data karyawan =====================")
        pool_conn = self.__get_conn()

        database_repo_postgresql = RepositoryPostgresql(pool_conn)

        logging.info(f"Create temp table karyawan")
        database_repo_postgresql.create_temp_table()

        logging.warning(f"Start inserting {len(data)} data into temp table")
        for i in range(0, len(data), self.__chunk_size):
            database_repo_postgresql.insert_temp_data(data[i:i+self.__chunk_size])

        logging.warning(f"Start upsert data from temp table to table karyawan")
        database_repo_postgresql.update_table_karyawan()

        logging.info(f"Drop temp table karyawan")
        database_repo_postgresql.delete_temp_table()

        self.__put_conn(pool_conn)
        self.__close_conn()
        logging.info(f"Successfully sync data karyawan")

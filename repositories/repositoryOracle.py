from database import get_connection_ora


class RepositoryOracle:
    def __init__(self):
        self.__conn = get_connection_ora()

    def get_all_data(self):
        conn = self.__conn.get_conn()
        try:
            cur = conn.cursor()
            sql = """
                select * from tbl_job_desc where id < 1000 and id > 0 limit 1000
            """
            cur.execute(sql)
            return cur.fetchall()
        except Exception as error:
            raise error
        finally:
            cur.close()
            conn.close()

import logging
from psycopg2.extras import execute_values


class RepositoryPostgresql:
    def __init__(self, conn):
        self.__conn = conn

    def create_temp_table(self):
        conn = self.__conn
        cur = conn.cursor()
        try:
            sql = """
                CREATE TABLE temp_tbl_karyawan (
                    id serial4 NOT NULL,
                    job_id varchar(17) NULL DEFAULT NULL::character varying,
                    job_company_id varchar(7) NULL DEFAULT NULL::character varying,
                    job_type varchar(15) NULL DEFAULT NULL::character varying,
                    job_degree varchar(15) NULL DEFAULT NULL::character varying,
                    job_major varchar(15) NULL DEFAULT NULL::character varying,
                    job_industry varchar(15) NULL DEFAULT NULL::character varying,
                    job_year_experiece numeric(2) NULL DEFAULT 0,
                    job_miles_from_metropolis numeric(3) NULL DEFAULT 0,
                    CONSTRAINT temp_tbl_karyawan_pkey PRIMARY KEY (id)
                )
            """
            cur.execute(sql)
            conn.commit()
        except Exception as error:
            conn.rollback()
            logging.critical(f"{error}")
        finally:
            cur.close()

    def insert_temp_data(self, data):
        conn = self.__conn
        cur = conn.cursor()
        try:
            sql = """
                INSERT INTO temp_tbl_karyawan VALUES %s
            """
            execute_values(cur, sql, data)
            conn.commit()
            logging.info(f"Successfully insert {len(data)} data")
        except Exception as error:
            conn.rollback()
            logging.critical(f"{error}")
        finally:
            cur.close()

    def update_table_karyawan(self):
        conn = self.__conn
        cur = conn.cursor()
        try:
            sql = """
                INSERT INTO tbl_karyawan(id, job_id, job_company_id, job_type, job_degree, job_major, job_industry, job_year_experiece, job_miles_from_metropolis) (
                    select * from temp_tbl_karyawan
                )
                ON CONFLICT (id) DO update SET 
                    job_id=excluded.job_id, job_company_id=excluded.job_company_id, job_type=excluded.job_type, 
                    job_degree=excluded.job_degree, job_major=excluded.job_major, job_industry=excluded.job_industry, 
                    job_year_experiece=excluded.job_year_experiece, job_miles_from_metropolis=excluded.job_miles_from_metropolis
            """
            cur.execute(sql)
            conn.commit()
            logging.info(f"Successfully upsert into table karyawan")
        except Exception as error:
            conn.rollback()
            logging.critical(f"{error}")
        finally:
            cur.close()

    def delete_temp_table(self):
        conn = self.__conn
        cur = conn.cursor()
        try:
            sql = """
                DROP TABLE temp_tbl_karyawan
            """
            cur.execute(sql)
            conn.commit()
        except Exception as error:
            conn.rollback()
            logging.critical(f"{error}")
        finally:
            cur.close()

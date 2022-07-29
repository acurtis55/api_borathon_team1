import psycopg2
from decouple import config


class DB:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host=config("ENDPOINT"),
                port=config("PORT"),
                database=config("DBNAME"),
                user=config("PSQL_AWS_USER"),
                password=config("PASSWORD"),
                sslrootcert=config("SSL_ROOT_PATH")
            )
            self.conn.set_session(autocommit=True)
        except Exception as e:
            print("Database connection failed due to {}".format(e))

    def exec(self, sql: str):
        cur = self.conn.cursor()
        cur.execute(sql)
        try:
            return cur.fetchall()
        except psycopg2.ProgrammingError:
            return

    def close(self):
        self.conn.close()

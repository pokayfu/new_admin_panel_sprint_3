from load_data import load_from_sqlite
import sqlite3
import psycopg2
from insert_data import InsertWorker
from settings import dsn, sql_path
from contextlib import contextmanager, closing


class SQLToPostgres:
    def __init__(self) -> None:
        self.Writer = InsertWorker()
        self.table_name_insert_function = {
            'person': self.Writer.insert_person,
            'film_work': self.Writer.insert_film_work,
            'genre': self.Writer.insert_genre,
            'genre_film_work': self.Writer.insert_genre_film_work_data,
            'person_film_work': self.Writer.insert_person_film_work_data
        }

    @contextmanager
    def conn_context(self, db_path: str):
        conn = sqlite3.connect(sql_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def run(self) -> None:
        with self.conn_context(db_path=sql_path) as conn, closing(psycopg2.connect(**dsn)) as pgconn:
            sqlite_curs = conn.cursor()
            pgcursor = pgconn.cursor()
            for table, insert_foo in self.table_name_insert_function.items():
                for table_row in load_from_sqlite(sqlite_curs, table_name=table):
                    insert_foo(cursor=pgcursor, item=table_row)
                    pgconn.commit()
        conn.close()

    def define_db_structure(self):
        with closing(psycopg2.connect(**dsn)) as pgconn:
            pgcursor = pgconn.cursor()
            sql = open('movies_database.ddl').read()
            pgcursor.execute(sql)
            pgconn.commit()
            
if __name__ == '__main__':
    sqltopostgres = SQLToPostgres()
    sqltopostgres.define_db_structure()
    sqltopostgres.run()
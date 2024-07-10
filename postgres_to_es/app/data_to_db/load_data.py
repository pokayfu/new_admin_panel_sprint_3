def load_from_sqlite(curs, table_name: str):
    num_lines = tuple(curs.execute(f"SELECT COUNT(*) FROM {table_name}"))[0]
    curs.execute(f"SELECT * FROM {table_name}")
    for _ in range(num_lines[0]):
        data = curs.fetchone()
        yield tuple(data)

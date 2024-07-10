class InsertWorker:
    def __init__(self) -> None:
        pass

    def insert_person(self, cursor, item: list) -> None:
        cursor.execute("""
            INSERT INTO content.person (id, full_name, created, modified)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """, item)

    def insert_film_work(self, cursor, item: list) -> None:
        cursor.execute("""
            INSERT INTO content.film_work (id, title, description,
                        creation_date, file_path,
                        rating, type, created, modified)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """, item)

    def insert_genre(self, cursor, item: list) -> None:
        cursor.execute("""
            INSERT INTO content.genre (id, name, description,
                        created, modified)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """, item)

    def insert_genre_film_work_data(self, cursor, item: list) -> None:
        cursor.execute("""
            INSERT INTO content.genre_film_work(id, film_work_id,
                        genre_id, created)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (film_work_id, genre_id) DO NOTHING
            """, item)

    def insert_person_film_work_data(self, cursor,
                                     item: list) -> None:
        cursor.execute("""
            INSERT INTO content.person_film_work(id, film_work_id,
                        person_id, role, created)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """, item)

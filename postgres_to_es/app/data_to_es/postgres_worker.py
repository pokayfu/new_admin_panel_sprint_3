from backoff import backoff
import psycopg2


class PostgresProducer:
    def __init__(self, conn: psycopg2.extensions.connection, extract_size: int) -> None:
        self.conn = conn
        self.extract_size = extract_size
        self.tables = ['film_work', 'person', 'genre']

    def check_updates(self, time: str):
        for table in self.tables:
            query = f"""
                SELECT id, modified
                FROM content.{table}
                WHERE modified > '{time}'
                ORDER BY modified;
                    """
            for packs in self.iter_table(query):
                entity_ids = [pack['id'] for pack in packs]
                modified_date = packs[0]['modified']
                yield table, entity_ids, modified_date
    
    @backoff()
    def iter_table(self, query: str):
        cursor = self.conn.cursor()
        cursor.execute(query)
        while lines := cursor.fetchmany(size=self.extract_size):
            yield [dict(line) for line in lines]  


class PostgresEnricher:
    def __init__(self, conn: psycopg2.extensions.connection) -> None:
        self.conn = conn
        self.related_tables = {
        'person': 'person_film_work',
        'genre': 'genre_film_work',
        'film_work': None
    }
    
    def enrich(self, table: str, entity_ids: list[str]):
        tables = ['person', 'genre']
        if table == 'film_work':
            return entity_ids
        if table in tables:
            lines_dict = self.pg_query_exec(
                conn=self.conn,
                query=self.get_right_query(table_name=table, ids=entity_ids)
            )
            encriched_data = [line['id'] for line in lines_dict]
            return encriched_data
    
    @backoff()
    def pg_query_exec(self, conn: psycopg2.extensions.connection, query: str) -> list[dict]:
        cursor = conn.cursor()
        cursor.execute(query)
        lines = cursor.fetchall()
        res = [dict(line) for line in lines]
        return res

    def get_right_query(self, table_name: str, ids: list[str]):
        ids = ''.join([ f"'{x}'," for x in ids])[:-1]
        return f"""
            SELECT fw.id
            FROM content.film_work fw
            LEFT JOIN content.{self.related_tables[table_name]} rt ON 
            rt.film_work_id = fw.id
            WHERE rt.{table_name}_id IN ({ids})
            ORDER BY modified;
        """


class PostgresMerger:
    def __init__(self, pgconn: psycopg2.extensions.connection) -> None:
        self.conn = pgconn

    def merge(self, data) -> list[dict]:
        res = []
        raw_data = self.pg_query_exec(
            conn=self.conn,
            query=self.get_right_query(data)
        )
        data_by_id = {}
        for line in raw_data:
            if line['id'] not in data_by_id:
                data_by_id[line['id']] = [line]
            else:
                data_by_id[line['id']].append(line)

        for id, data in data_by_id.items():
            persons = [
            {
                'person_id': part['person_id'],
                'person_role': part['person_role'],
                'person_full_name': part['person_full_name'],
            }
            for part in data]
            genre_names = [part['genre_name'] for part in data]
            res.append({
                'id': id,
                'title': data[0]['title'],
                'description': data[0]['description'],
                'rating': data[0]['rating'],
                'type': data[0]['type'],
                'created': data[0]['created'],
                'modified': data[0]['modified'],
                'genres': list(set(genre_names)),
                'persons': persons
            })
        return res

    def get_right_query(self, film_work_ids: list[str]):
        ids = ''.join([ f"'{x}'," for x in film_work_ids])[:-1]
        return f"""
            SELECT
            fw.id,
            fw.title,
            fw.description,
            fw.rating,
            fw.type,
            fw.created,
            fw.modified,
            pfw.role as person_role,
            p.id as person_id,
            p.full_name as person_full_name,
            g.name as genre_name
            FROM content.film_work fw
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.person p ON p.id = pfw.person_id
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
            LEFT JOIN content.genre g ON g.id = gfw.genre_id
            WHERE fw.id IN ({ids});
        """

    @backoff()
    def pg_query_exec(self, conn: psycopg2.extensions.connection, query: str) :
        cursor = conn.cursor()
        cursor.execute(query)
        lines = cursor.fetchall()
        result_data =  [dict(line) for line in lines]
        return result_data
    
import time
import psycopg2
from state import State, JsonFileStorage
from settings import settings
from backoff import backoff
from transform import Transformer
from postgres_worker import PostgresProducer, PostgresEnricher, PostgresMerger
from contextlib import closing
from settings import dsn
import logging
import sys
from contextlib import closing
from elastic_load import ElasticLoader
import psycopg2.extras


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(level=logging.INFO)
logger.addHandler(handler)


class ETL_Worker:
    def __init__(self) -> None:
        self.state = State(storage=JsonFileStorage(file_path=settings['storage_file_path']))
        self.loader = ElasticLoader(
                service_host=settings['elastic_host'],
                service_port=settings['elastic_port'],
                index=settings['elastic_index']
            )
        self.sleeping_time = settings['etl_sleep_time']
        self.nap_time = settings['etl_nap_time']

    @backoff()
    def run(self) -> None:
        logger.info('ETL started')
        with closing(psycopg2.connect(**dsn, cursor_factory=psycopg2.extras.DictCursor)) as pgconn:
            producer = PostgresProducer(conn=pgconn, extract_size=settings['etl_extract_size'])
            enricher = PostgresEnricher(conn=pgconn)
            merger = PostgresMerger(pgconn=pgconn)
            while True:
                updated_time = self.state.get_state('modified')
                if not updated_time:
                    updated_time = settings['etl_start_time']
                updates = producer.check_updates(time=updated_time)
                for updated_table, updated_entities, modified in updates:
                    enriched_data = enricher.enrich(table=updated_table, entity_ids=updated_entities)
                    merged_data = merger.merge(enriched_data)
                    transformed_data = Transformer().transform(merged_data)
                    self.loader.upload(transformed_data)
                    self.state.set_state(key='modified', value=modified.strftime('%Y-%m-%d %H:%M:%S.%f %z'))
                    logger.info("updated %s, sleep for %s sec", len(transformed_data), self.sleeping_time)
                    time.sleep(self.sleeping_time)
                logger.info("no updates found, sleep for %s seconds", self.nap_time)
                time.sleep(self.nap_time)


if __name__ == '__main__':
    ETL_Worker().run()

from models import Settings, PostgresSettings
import os
from dotenv import load_dotenv
load_dotenv()


settings =  Settings.model_validate({
    'storage_file_path' :  os.environ.get('STORAGE_FILE_PATH'),
    'elastic_host' :  os.environ.get('ELASTIC_HOST'),
    'elastic_port' :  os.environ.get('ELASTIC_PORT'),
    'elastic_index' :  os.environ.get('ELASTIC_INDEX'),
    'etl_start_time' :  os.environ.get('ETL_START_TIME'),
    'etl_extract_size' :  os.environ.get('ETL_EXTRACT_SIZE'),
    'etl_nap_time' :  os.environ.get('ETL_NAP_TIME'),
    'etl_sleep_time' :  os.environ.get('ETL_SLEEP_TIME')
    }).model_dump()



dsn =  PostgresSettings.model_validate({
    'dbname': os.environ.get('POSTGRES_DB'),
    'user': os.environ.get('POSTGRES_USER'),
    'password': os.environ.get('POSTGRES_PASSWORD'),
    'host': os.environ.get('POSTGRES_HOST'),
    'port': os.environ.get('POSTGRES_PORT')
}).model_dump()

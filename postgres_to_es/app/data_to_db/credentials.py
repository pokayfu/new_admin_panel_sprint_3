import os
from dotenv import load_dotenv
load_dotenv()


dsn_creds = {
    'db_name': os.environ.get('POSTGRES_DB'),
    'db_user': os.environ.get('POSTGRES_USER'),
    'db_pswd': os.environ.get('POSTGRES_PASSWORD'),
    'host': os.environ.get('POSTGRES_HOST'),
    'port': os.environ.get('POSTGRES_PORT')
}

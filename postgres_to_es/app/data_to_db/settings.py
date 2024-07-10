from credentials import dsn_creds

dsn = {'dbname': dsn_creds['db_name'],
        'user': dsn_creds['db_user'],
        'password': dsn_creds['db_pswd'],
        'host': dsn_creds['host'],
        'port': dsn_creds['port']}

sql_path = 'db.sqlite'

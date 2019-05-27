import psycopg2
import os
db_password = os.environ.get('CLOUD_SQL_PASSWORD')

def query_db(query='SELECT NOW() as now;'):
    """
    query psycopg2 db on relna project
    """
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        host = '/cloudsql/{}'.format(db_connection_name)
    else:
        # If running locally, use the TCP connections instead
        # Set up Cloud SQL Proxy (cloud.google.com/sql/docs/mysql/sql-proxy)
        # so that your application can use 127.0.0.1:3306 to connect to your
        # Cloud SQL instance
        host = '127.0.0.1'

    cnx = psycopg2.connect("sslmode=disable dbname=postgres user=postgres hostaddr=104.199.68.166 password={}".format(db_password))

    with cnx.cursor() as cursor:
        cursor.execute(query)
        try: result = cursor.fetchall()
        except psycopg2.ProgrammingError:
            pass #no results to fetch
    cnx.commit()
    cnx.close()

    try: return result
    except: return None

def get_imitation_learning_jobs():
    return query_db("SELECT * FROM imitation_learning_jobs")

def insert_imitation_learning_job(gym,expert_policy,python_model):
    """
    postgres=> SELECT * from imitation_learning_jobs;
       gym    | expert_policy |     python_model     | jobid
       ----------+---------------+----------------------+-------
       test_gym | test_policy   | print("hello world") |     1
       test_gym | test_policy   | print("hello world") |     2
       (2 rows)
    """
    return query_db("INSERT INTO imitation_learning_jobs \
            (gym, expert_policy, python_model) \
            values ('{}', '{}', '{}');".format(
        gym,
        expert_policy,
        python_model)
        )

import psycopg2
import os
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

def query_db(query='SELECT NOW() as now;'):
    """
    query psycopg2 db on relna project

    ###########FAIL TO AUTHENTICATE LOCALLY#######
    you need to export password
    export CLOUD_SQL_PASSWORD=""
    """
    if os.environ.get('GAE_ENV') == 'standard':
        # If deployed, use the local socket interface for accessing Cloud SQL
        host = '/cloudsql/{}'.format(db_connection_name)
        cnx = psycopg2.connect(dbname=db_name, user=db_user,
                                password=db_password, host=host)
    else:
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

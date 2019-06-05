import psycopg2
import os
db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

def query_db(query='SELECT NOW() as now;', args=None):
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
        cursor.execute(query,args)
        try: result = cursor.fetchall()
        except psycopg2.ProgrammingError:
            pass #no results to fetch
    cnx.commit()
    cnx.close()

    try: return result
    except: return None

def get_imitation_learning_jobs():
    return query_db("SELECT * FROM imitation_learning_jobs")

def insert_imitation_learning_job(
        gym,
        expert_policy,
        python_model,
        zipped_python_filename,
        trainer_package_filename):
    """
    COLUMNS:
     gym             | character varying(255) 
     expert_policy   | character varying(255) 
     python_model    | text                   
     jobid           | integer                
     zipped_python   | bytea                  
     trainer_package | bytea                  
    """
    zipped_python = open(zipped_python_filename, 'rb').read()
    trainer_package = open(trainer_package_filename, 'rb').read()
    return query_db("INSERT INTO imitation_learning_jobs \
            (gym, expert_policy, python_model, \
            zipped_python, trainer_package) \
            values (%s, %s, %s, %s, %s);", (
            gym,
            expert_policy,
            python_model,
            psycopg2.Binary(zipped_python),
            psycopg2.Binary(trainer_package)
            )
        )

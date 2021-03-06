import psycopg2
import os
import logging
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
        if args is not None and \
                (len(args) == 1 or (type(args) is not tuple and type(args) is not list)):
            # this is to avoid Psycopg2 - not all arguments converted during string formatting
            # https://stackoverflow.com/questions/
            # 47956425/psycopg2-not-all-arguments-converted-during-string-formatting
            cursor.execute(query,(args,))
        else:
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

def get_imitation_learning_job_pkg(job_id):
    """
    args:
        job_id: (int) e.g. 5

    returns:
        <class 'memoryview'> : bytes obj
    return pkg as a str (not on filesys since can't IO on filesys in prod)
    """
    query_result = query_db("select trainer_package from imitation_learning_jobs where jobid = %s;", str(job_id))
    return query_result[0][0]

def get_imitation_learning_job_code(job_id):
    """
    args:
        job_id: (int) e.g. 5

    returns:
        <class 'memoryview'> : bytes obj
    return zip code as a str (not on filesys since can't IO on filesys in prod)
    """
    query_result = query_db("select zipped_python from imitation_learning_jobs where jobid = %s;", str(job_id))
    return query_result[0][0]

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
    logging.warning("relna:relna:db - inserting new jobs from file")
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

def insert_imitation_learning_job_bytes(
        gym,
        expert_policy,
        python_model,
        zipped_python_binary,
        trainer_package_binary):
    """
    COLUMNS:
     gym             | character varying(255) 
     expert_policy   | character varying(255) 
     python_model    | text                   
     jobid           | integer                
     zipped_python   | bytea                  
     trainer_package | bytea                  
    """
    logging.warning("relna:relna:db - inserting new jobs from binaries")
    zipped_python = zipped_python_binary
    trainer_package = trainer_package_binary
    query_result = query_db("INSERT INTO imitation_learning_jobs \
            (gym, expert_policy, python_model, \
            zipped_python, trainer_package) \
            values (%s, %s, %s, %s, %s) RETURNING jobid;", (
            gym,
            expert_policy,
            python_model,
            psycopg2.Binary(zipped_python),
            psycopg2.Binary(trainer_package)
            )
        )
    return query_result[0][0]

def update_imitation_learning_job_output(
        jobid,
        output_1,
        output_2
        ):
    """
    """
    logging.warning("relna:relna:db - updating job output values")
    return query_db("UPDATE imitation_learning_jobs SET \
            output_1 = %s, \
            output_2 = %s  \
            WHERE jobid = %s;", (
                output_1,
                output_2,
                jobid
                ))

import psycopg2

connection = None
try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "root",
                                  host = "172.17.0.2",
                                  port = "5432",
                                  database = "ebook")

    cursor = connection.cursor()
    # Print PostgreSQL Connection properties
    print (connection.get_dsn_parameters(), "\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")
    cursor.execute("select * from pictures where id=97")
    id = ''
    name = ''
    path = ''
    for row in cursor.fetchall():
        id, name, path = row[0], row[1], row[2]
    print id, name, path

    import os
    if os.path.exists(path) :
        print 'qcq'

except (Exception, psycopg2.Error) as error:
    print ("Error while connecting to PostgreSQL", error)
finally:
    # closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

import mysql.connector
import sshtunnel
import logging
from sshtunnel import SSHTunnelForwarder

# Global - Connection strings for ssh and db

# Connection to machine
ssh_host = '[IP or HOST]'
ssh_username = '[username]'
ssh_password = '[password]'

# Connection to db
database_username = '[db_username]'
database_password = '[db_password]'
database_name = '[db_name]'
localhost = '127.0.0.1'

def open_ssh_tunnel(verbose=False):
    """Open an SSH tunnel and connect using a username and password.
    
    :param verbose: Set to True to show logging
    :return tunnel: Global SSH tunnel connection
    """
    
    if verbose:
        sshtunnel.DEFAULT_LOGLEVEL = logging.DEBUG
    
    global tunnel
    tunnel = SSHTunnelForwarder(
        (ssh_host, 22),
        ssh_username = ssh_username,
        ssh_password = ssh_password,
        remote_bind_address = ('127.0.0.1', 3306)
    )
    
    tunnel.start()

def query_db(verbose=False):

    mydb = mysql.connector.connect(
        host = localhost,
        port= tunnel.local_bind_port,
        user = database_username,
        passwd = database_password,
        database= database_name
    )

    cursor = mydb.cursor(dictionary=True)
    query = "[SQL Query]"

    cursor.execute(query)
    myresult = cursor.fetchall()

    for x in myresult:
        print(x['[field]'])

    mydb.close()

def close_ssh_tunnel():
    """Closes the SSH tunnel connection.
    """
    
    tunnel.close

def main():

    open_ssh_tunnel()
    query_db()
    close_ssh_tunnel()

if __name__ == '__main__':
    main()

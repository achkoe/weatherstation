import paramiko
import argparse
from dotenv import dotenv_values
from common import DBPATH, DBNAME

FOLDER = "weatherstation"
REMOTE_FILE = f'/{FOLDER}/{DBNAME}'


def backup_db(read_only: bool):
    secrets = dotenv_values(".env")
    hostname = secrets["HOSTNAME"] 
    port = secrets["PORT"] 
    username = secrets["USERNAME"] 
    password = secrets["PASSWORD"]

    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the SFTP server
    ssh_client.connect(hostname, port, username, password)

    # Create an SFTP session
    sftp = ssh_client.open_sftp()
    files = sftp.listdir()

    if FOLDER not in files:
        sftp.mkdir(FOLDER)
        files = sftp.listdir()
        
    assert FOLDER in files
    
    if not read_only:
        sftp.put(str(DBPATH), REMOTE_FILE)
        print(f"{str(DBPATH)} written to {REMOTE_FILE}")

    stat = sftp.stat(REMOTE_FILE)
    print(f"{DBNAME} -> {stat}")


    sftp.close()
    ssh_client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backup Database")
    parser.add_argument("-r", "--read", action="store_true", help="read information from backup server")
    args = parser.parse_args()
    backup_db(args.read)
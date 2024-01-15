import subprocess
import datetime
import os


db_host = "localhost"
db_port = "5432"
db_name = "seller_project"
db_user = ""  # Replace with db username
db_password = ""  # Replace with db password

# Backup directory
backup_dir = "/db/backups"

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
backup_file = f"{backup_dir}/backup_{timestamp}.sql"

# Command to create the backup using pg_dump
command = [
    "pg_dump",
    f"--host={db_host}",
    f"--port={db_port}",
    f"--username={db_user}",
    f"--dbname={db_name}",
    f"--file={backup_file}",
]

# If your PostgreSQL server requires a password, you can pass it using the PGPASSWORD environment variable
if db_password:
    os.environ["PGPASSWORD"] = db_password

try:
    subprocess.run(command, check=True)
    print(f"Backup created successfully: {backup_file}")
except subprocess.CalledProcessError as e:
    print(f"Error creating backup: {e}")
finally:
    # Clean up the environment variable if it was set
    if "PGPASSWORD" in os.environ:
        del os.environ["PGPASSWORD"]

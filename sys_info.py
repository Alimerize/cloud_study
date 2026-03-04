import os
import boto3
import getpass
import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    host="localhost",
    database="cloud_study",
    user="alimerize",
    password="mysecretpassword"
)

cursor = conn.cursor()
user_name = getpass.getuser()
now = datetime.now()

console_out = f"Пользователь {user_name} запустил проверку системы"
print(console_out)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id  SERIAL PRIMARY KEY,
        message TEXT
    );
""")
conn.commit()

cursor.execute("INSERT INTO logs (message) VALUES (%s)", (console_out,))
conn.commit()
print(f"✅ База: Данные сохранены.")

status_file = "status.txt"
with open(status_file, "w") as f:
    f.write("Система работает стабильно")

s3 = boto3.client(
    's3',
    endpoint_url = 'http://localhost:4566',
    aws_access_key_id = 'test',
    aws_secret_access_key = 'test'
)

try: 
    s3.create_bucket(Bucket="my-test-bucket")
    print("✅ S3: Бакет создан или уже был.")
except Exception: 
    pass

s3.upload_file(status_file, "my-test-bucket", "daily_status.txt")
print("✅ S3: Отчет доставлен!")

cursor.close()
conn.close()

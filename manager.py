import boto3
import psycopg2
from datetime import datetime

# 1. ПОДКЛЮЧАЕМСЯ К БАЗЕ (Библиотекарь)
try:
    conn = psycopg2.connect(
        host="localhost", 
        database="cloud_study", 
        user="alimerize", 
        password="mysecretpassword"
    )
    cursor = conn.cursor()
    
    # Записываем событие в таблицу logs
    now = datetime.now()
    cursor.execute("INSERT INTO logs (message) VALUES (%s)", (f"Запуск скрипта в {now}",))
    conn.commit()
    print("✅ База данных: Событие зафиксировано.")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"❌ Ошибка базы: {e}")

# 2. ОТПРАВЛЯЕМ ФАЙЛ В ОБЛАКО (Курьер)
try:
    s3 = boto3.client('s3', endpoint_url='http://localhost:4566', 
                      aws_access_key_id='test', aws_secret_access_key='test')

    # ВНИМАНИЕ: Имя бакета, который создал TERRAFORM
    TARGET_BUCKET = "success-storage-2026"
    
    s3.upload_file("hello.txt", TARGET_BUCKET, "final_report.txt")
    print(f"✅ S3: Файл 'hello.txt' доставлен в бакет '{TARGET_BUCKET}'.")
except Exception as e:
    print(f"❌ Ошибка S3: {e}")


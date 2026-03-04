import os
import boto3
import psycopg2

# 1. ПОДКЛЮЧАЕМСЯ
conn = psycopg2.connect(
    host="localhost",
    database="cloud_study",
    user="alimerize",
    password="mysecretpassword"
)
cursor = conn.cursor()

# 2. ШПИОН (OS): Собираем данные
files = os.listdir(".")
count = len(files)

# СОЗДАЕМ ТЕКСТ ДЛЯ БАЗЫ (в зависимости от количества)
if count > 5:
    db_message = f"Внимание! Папка заполнена, файлов: {count}"
else:
    db_message = f"Всё в норме, файлов: {count}"

print(db_message) # Вывод в консоль

# 3. ПЕРЕВОДЧИК (SQL): Пишем в базу НАШЕ СООБЩЕНИЕ
cursor.execute("INSERT INTO logs (message) VALUES (%s)", (db_message,))
conn.commit()
print(f"✅ База: Данные сохранены.")

# 4. СОЗДАЕМ ОТЧЕТ
report_file = "report.txt"
with open(report_file, "w") as f: # Используем "w", чтобы файл не раздувался бесконечно
    # Превращаем список ['1.py', '2.py'] в текст через запятую
    f.write(f"Список файлов: {', '.join(files)}")

# 5. КУРЬЕР (BOTO3)
s3 = boto3.client(
    's3',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

# Загружаем наш свежий отчет
s3.upload_file(report_file, "my-test-bucket", "final_report.txt")
print("✅ S3: Отчет доставлен!")

cursor.close()
conn.close()

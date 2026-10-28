"""Script tạo database MySQL cho dự án BookStore."""
import MySQLdb

conn = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", password="")
cursor = conn.cursor()
sql = "CREATE DATABASE IF NOT EXISTS bookstore_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
cursor.execute(sql)
print("[OK] Database 'bookstore_db' ready.")
conn.close()


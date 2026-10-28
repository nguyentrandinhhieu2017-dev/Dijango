"""Kiểm tra các bảng đã migrate vào bookstore_db."""
import MySQLdb

conn = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", password="", db="bookstore_db")
cursor = conn.cursor()
cursor.execute("SHOW TABLES")
tables = [row[0] for row in cursor.fetchall()]
print(f"[OK] {len(tables)} tables in bookstore_db:")
for t in tables:
    cursor.execute(f"SELECT COUNT(*) FROM `{t}`")
    count = cursor.fetchone()[0]
    print(f"     {t:<40} ({count} rows)")
conn.close()


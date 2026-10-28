"""
Script tạo superuser mặc định cho môi trường dev.
Chạy: python create_superuser.py
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BookStore.settings")
django.setup()

from django.contrib.auth.models import User

username = "admin"
email = "admin@bookstore.com"
password = "admin123"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"[OK] Superuser created: {username} / {password}")
else:
    print(f"[INFO] Superuser '{username}' already exists.")

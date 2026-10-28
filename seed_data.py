# -*- coding: utf-8 -*-
"""

seed_data.py — Tạo dữ liệu mẫu cho dự án BookStore.
Chạy: python seed_data.py
"""

import os
import sys

# Đảm bảo in unicode ra console trên Windows
sys.stdout.reconfigure(encoding='utf-8')

# ── 1. Thiết lập môi trường Django ──────────────────────────────────────────
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BookStore.settings")

import django
django.setup()

# ── 2. Import models ─────────────────────────────────────────────────────────
from store.models import Category, Book

# ── 3. Xóa dữ liệu cũ (Book trước vì có FK → Category) ─────────────────────
Book.objects.all().delete()
Category.objects.all().delete()
print("  [clear] Đã xóa dữ liệu cũ.")

# ── 4. Tạo danh mục ──────────────────────────────────────────────────────────
categories_data = [
    "Lập trình & Công nghệ",
    "Tiểu thuyết",
    "Khoa học & Khám phá",
    "Kỹ năng & Phát triển bản thân",
]

cats = {}
for name in categories_data:
    cat = Category.objects.create(name=name)
    cats[name] = cat
    print(f"  [category] + {name}")

# ── 5. Tạo sách ──────────────────────────────────────────────────────────────
books_data = [
    # ── Lập trình & Công nghệ ──────────────────────────────────────────────
    {
        "title": "Clean Code: Nghệ thuật viết code sạch",
        "author": "Robert C. Martin",
        "price": 320000,
        "stock": 45,
        "category": "Lập trình & Công nghệ",
        "description": (
            "Cuốn sách kinh điển về viết code sạch, dễ đọc và dễ bảo trì. "
            "Robert C. Martin hướng dẫn lập trình viên cách tổ chức code, đặt tên biến, "
            "viết hàm và xử lý lỗi một cách chuyên nghiệp nhất."
        ),
    },
    {
        "title": "Python Crash Course: Lập trình Python từ căn bản",
        "author": "Eric Matthes",
        "price": 275000,
        "stock": 60,
        "category": "Lập trình & Công nghệ",
        "description": (
            "Cuốn sách nhập môn Python lý tưởng cho người mới bắt đầu. "
            "Bao gồm các dự án thực tế: trò chơi, trực quan hóa dữ liệu và ứng dụng web."
        ),
    },
    {
        "title": "Django for Professionals: Xây dựng ứng dụng cấp độ Production",
        "author": "William S. Vincent",
        "price": 299000,
        "stock": 30,
        "category": "Lập trình & Công nghệ",
        "description": (
            "Hướng dẫn xây dựng ứng dụng web Django cấp độ production với Docker, "
            "PostgreSQL, Stripe và các best practice bảo mật hiện đại."
        ),
    },
    {
        "title": "Kiến trúc phần mềm: Từ thiết kế đến triển khai",
        "author": "Mark Richards & Neal Ford",
        "price": 350000,
        "stock": 22,
        "category": "Lập trình & Công nghệ",
        "description": (
            "Khám phá các kiểu kiến trúc phần mềm phổ biến: microservices, event-driven, "
            "layered và pipeline. Tác giả cung cấp bộ tiêu chí đánh giá giúp bạn lựa chọn "
            "kiến trúc phù hợp cho từng bài toán thực tế."
        ),
    },
    {
        "title": "Học máy thực chiến với Python và Scikit-Learn",
        "author": "Aurélien Géron",
        "price": 420000,
        "stock": 18,
        "category": "Lập trình & Công nghệ",
        "description": (
            "Hướng dẫn toàn diện về Machine Learning từ lý thuyết đến thực hành. "
            "Bao gồm hồi quy, phân loại, học sâu và triển khai mô hình với TensorFlow và Keras."
        ),
    },
    # ── Tiểu thuyết ───────────────────────────────────────────────────────
    {
        "title": "Nhà Giả Kim",
        "author": "Paulo Coelho",
        "price": 89000,
        "stock": 120,
        "category": "Tiểu thuyết",
        "description": (
            "Câu chuyện về cậu bé Santiago hành trình tìm kho báu và khám phá "
            "ý nghĩa cuộc sống. Một trong những cuốn sách bán chạy nhất mọi thời đại "
            "với hơn 150 triệu bản in trên toàn thế giới."
        ),
    },
    {
        "title": "Đắc Nhân Tâm",
        "author": "Dale Carnegie",
        "price": 95000,
        "stock": 85,
        "category": "Tiểu thuyết",
        "description": (
            "Tác phẩm kinh điển về nghệ thuật giao tiếp và lấy lòng người khác. "
            "Các nguyên tắc được trắc nghiệm qua nhiều thế hệ, giúp bạn xây dựng "
            "mối quan hệ tốt đẹp trong cuộc sống và công việc."
        ),
    },
    {
        "title": "Tuổi Trẻ Đáng Giá Bao Nhiêu",
        "author": "Rosie Nguyễn",
        "price": 110000,
        "stock": 75,
        "category": "Tiểu thuyết",
        "description": (
            "Cuốn sách dành cho những bạn trẻ đang bước vào ngưỡng cửa cuộc đời, "
            "đang băn khoăn về định hướng tương lai và muốn sống một cuộc đời ý nghĩa. "
            "Rosie Nguyễn chia sẻ những bài học thực tế từ chính hành trình trưởng thành của mình."
        ),
    },
    {
        "title": "Cà Phê Cùng Tony",
        "author": "Tony Buổi Sáng",
        "price": 98000,
        "stock": 65,
        "category": "Tiểu thuyết",
        "description": (
            "Tập hợp những bài viết thẳng thắn, hài hước và đầy tâm huyết của Tony Buổi Sáng "
            "về cuộc sống, công việc và cách người trẻ Việt Nam cần thay đổi tư duy "
            "để thành công trong thế giới hội nhập."
        ),
    },
    # ── Khoa học & Khám phá ────────────────────────────────────────────────
    {
        "title": "Lược sử thời gian: Từ Vụ Nổ Lớn đến Hố Đen",
        "author": "Stephen Hawking",
        "price": 185000,
        "stock": 40,
        "category": "Khoa học & Khám phá",
        "description": (
            "Stephen Hawking dẫn dắt người đọc qua hành trình khám phá vũ trụ: "
            "từ Big Bang đến lỗ đen, từ lượng tử đến thuyết tương đối. "
            "Cuốn sách khoa học bán chạy nhất trong lịch sử xuất bản."
        ),
    },
    {
        "title": "Sapiens: Lược sử loài người",
        "author": "Yuval Noah Harari",
        "price": 225000,
        "stock": 55,
        "category": "Khoa học & Khám phá",
        "description": (
            "Từ thời kỳ đồ đá đến thế kỷ 21, Harari khám phá cách Homo Sapiens "
            "chinh phục Trái Đất nhờ ngôn ngữ, tiền tệ, tôn giáo và khoa học. "
            "Một cuốn sách làm thay đổi cách nhìn của bạn về bản thân và xã hội."
        ),
    },
    {
        "title": "Vũ trụ trong vỏ hạt dẻ",
        "author": "Stephen Hawking",
        "price": 175000,
        "stock": 28,
        "category": "Khoa học & Khám phá",
        "description": (
            "Tiếp nối 'Lược sử thời gian', Hawking đưa bạn vào hành trình khám phá "
            "siêu dây, M-lý thuyết, vũ trụ siêu dây và các chiều không gian ẩn "
            "qua những hình minh họa đẹp mắt và cách giải thích đơn giản."
        ),
    },
    # ── Kỹ năng & Phát triển bản thân ─────────────────────────────────────
    {
        "title": "Atomic Habits: Thói quen nguyên tử",
        "author": "James Clear",
        "price": 149000,
        "stock": 95,
        "category": "Kỹ năng & Phát triển bản thân",
        "description": (
            "Hệ thống thực tế để xây dựng thói quen tốt và phá bỏ thói quen xấu. "
            "James Clear chỉ ra rằng sự thay đổi lớn bắt đầu từ những cải tiến nhỏ 1% "
            "mỗi ngày và cách thiết kế môi trường hỗ trợ hành vi tích cực."
        ),
    },
    {
        "title": "Mindset: Tư duy phát triển",
        "author": "Carol S. Dweck",
        "price": 165000,
        "stock": 42,
        "category": "Kỹ năng & Phát triển bản thân",
        "description": (
            "Nhà tâm lý học Stanford Carol Dweck chứng minh rằng tư duy cố định hay "
            "tư duy phát triển ảnh hưởng sâu sắc đến mọi khía cạnh của cuộc sống. "
            "Học cách nuôi dưỡng tư duy tăng trưởng để đạt thành công bền vững."
        ),
    },
    {
        "title": "Đọc vị bất kỳ ai",
        "author": "David J. Lieberman",
        "price": 128000,
        "stock": 50,
        "category": "Kỹ năng & Phát triển bản thân",
        "description": (
            "Các kỹ thuật tâm lý học được FBI và CIA áp dụng để nhận biết ý định thật "
            "sự của con người qua ngôn ngữ cơ thể, lời nói và hành vi. "
            "Giúp bạn đưa ra quyết định sáng suốt hơn trong các mối quan hệ."
        ),
    },
    {
        "title": "Nghệ thuật tinh tế của việc đếch quan tâm",
        "author": "Mark Manson",
        "price": 135000,
        "stock": 88,
        "category": "Kỹ năng & Phát triển bản thân",
        "description": (
            "Cách tiếp cận phản trực giác để sống một cuộc đời tốt đẹp hơn. "
            "Mark Manson lập luận rằng chìa khóa của hạnh phúc không phải là quan tâm "
            "đến mọi thứ mà là biết quan tâm đúng thứ và bỏ qua những thứ còn lại."
        ),
    },
    {
        "title": "Tư duy nhanh và chậm",
        "author": "Daniel Kahneman",
        "price": 255000,
        "stock": 35,
        "category": "Kỹ năng & Phát triển bản thân",
        "description": (
            "Nhà tâm lý học đoạt giải Nobel giải thích hai hệ thống tư duy chi phối "
            "quyết định của con người: tư duy nhanh (bản năng) và tư duy chậm (lý trí). "
            "Khám phá cách nhận ra và tránh các thiên kiến nhận thức trong cuộc sống hàng ngày."
        ),
    },
]

for data in books_data:
    Book.objects.create(
        title=data["title"],
        author=data["author"],
        price=data["price"],
        stock=data["stock"],
        description=data["description"],
        category=cats[data["category"]],
    )
    print(f"  [book]     + {data['title']}")

# ── 6. Tổng kết ───────────────────────────────────────────────────────────────
print()
print("=" * 60)
print(f"  Đã thêm {Category.objects.count()} danh mục")
print(f"  Đã thêm {Book.objects.count()} cuốn sách")
print("  Đã thêm dữ liệu thành công!")
print("=" * 60)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from .models import Book, Category, Purchase, Wallet
from .forms import RegisterForm


def home(request):
    """Trang chủ — truy cập tự do."""
    featured_books = Book.objects.select_related("category").all()[:6]
    categories = Category.objects.all()
    return render(request, "store/home.html", {
        "featured_books": featured_books,
        "categories": categories,
    })


def book_list(request):
    """Danh sách sách — truy cập tự do."""
    category_id = request.GET.get("category")
    books = Book.objects.select_related("category").all()
    categories = Category.objects.all()

    if category_id:
        books = books.filter(category_id=category_id)

    return render(request, "store/book_list.html", {
        "books": books,
        "categories": categories,
        "selected_category": category_id,
    })


def book_detail(request, pk):
    """Chi tiết sách — yêu cầu đăng nhập."""
    book = get_object_or_404(Book, pk=pk)
    if not request.user.is_authenticated:
        messages.warning(request, "Vui lòng đăng nhập để xem chi tiết sách.")
        return redirect("store:login")
    return render(request, "store/book_detail.html", {"book": book})


@login_required
@transaction.atomic
def buy_book(request, pk):
    """
    Xử lý giao dịch mua sách an toàn với @transaction.atomic:
    - Kiểm tra sách còn tồn kho (stock > 0)
    - Kiểm tra số dư ví người dùng (wallet.balance >= book.price)
    - Trừ tiền ví, trừ tồn kho và ghi nhận đơn mua Purchase.
    """
    if request.method != "POST":
        return redirect("store:book_detail", pk=pk)

    # Khóa bản ghi với select_for_update để tránh race condition khi nhiều request đồng thời
    book = get_object_or_404(Book.objects.select_for_update(), pk=pk)
    wallet, _ = Wallet.objects.select_for_update().get_or_create(user=request.user)

    # 1. Kiểm tra tồn kho
    if book.stock <= 0:
        messages.error(request, f"Rất tiếc, cuốn sách '{book.title}' hiện đã hết hàng trong kho!")
        return redirect("store:book_detail", pk=pk)

    # 2. Kiểm tra số dư ví
    book_price_int = int(book.price)
    if wallet.balance < book_price_int:
        messages.error(
            request,
            f"Số dư trong ví không đủ để thanh toán ({wallet.balance:,} VNĐ / Giá sách: {book_price_int:,} VNĐ). Vui lòng nạp thêm tiền!"
        )
        return redirect("store:book_detail", pk=pk)

    # 3. Trừ tiền ví và trừ tồn kho sách
    wallet.balance -= book_price_int
    wallet.save()

    book.stock -= 1
    book.save()

    # 4. Ghi nhận giao dịch mua sách
    Purchase.objects.create(user=request.user, book=book)

    messages.success(
        request,
        f"Thanh toán thành công! Bạn đã mua cuốn sách '{book.title}' với giá {book_price_int:,} VNĐ. Số dư còn lại: {wallet.balance:,} VNĐ."
    )
    return redirect("store:my_books")


@login_required
def add_funds(request):
    """View nạp tiền vào ví điện tử (phục vụ mục đích test giao dịch)."""
    wallet, _ = Wallet.objects.get_or_create(user=request.user)

    if request.method == "POST":
        try:
            amount = int(request.POST.get("amount", 0))
            if amount <= 0:
                messages.error(request, "Số tiền nạp vào ví phải lớn hơn 0 VNĐ.")
            else:
                wallet.balance += amount
                wallet.save()
                messages.success(request, f"Nạp thành công {amount:,} VNĐ vào ví! Số dư hiện tại: {wallet.balance:,} VNĐ.")
                next_url = request.GET.get("next")
                if next_url:
                    return redirect(next_url)
                return redirect("store:add_funds")
        except (ValueError, TypeError):
            messages.error(request, "Vui lòng nhập số tiền hợp lệ.")

    return render(request, "store/add_funds.html", {
        "wallet": wallet,
    })


@login_required
def my_books(request):
    """Trang Sách của bạn — hiển thị danh sách sách người dùng đã mua."""
    purchases = Purchase.objects.filter(user=request.user).select_related("book", "book__category").order_by("-purchased_at")
    return render(request, "store/my_books.html", {
        "purchases": purchases,
    })


def register_view(request):
    """Đăng ký tài khoản khách hàng."""
    if request.user.is_authenticated:
        return redirect("store:home")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Chào mừng {user.username}! Đăng ký thành công.")
        return redirect("store:home")

    return render(request, "store/register.html", {"form": form})


def login_view(request):
    """Đăng nhập."""
    if request.user.is_authenticated:
        return redirect("store:home")

    form = AuthenticationForm(data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f"Xin chào, {user.username}!")
        next_url = request.GET.get("next", "store:home")
        return redirect(next_url)

    return render(request, "store/login.html", {"form": form})


@login_required
def logout_view(request):
    """Đăng xuất."""
    logout(request)
    messages.info(request, "Bạn đã đăng xuất.")
    return redirect("store:home")


@login_required
def profile_view(request):
    """Trang cá nhân — yêu cầu đăng nhập."""
    wallet, _ = Wallet.objects.get_or_create(user=request.user)
    return render(request, "store/profile.html", {
        "user": request.user,
        "wallet": wallet,
    })

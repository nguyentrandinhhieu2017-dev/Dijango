from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên danh mục")

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=300, verbose_name="Tiêu đề")
    author = models.CharField(max_length=200, verbose_name="Tác giả")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá")
    stock = models.PositiveIntegerField(default=0, verbose_name="Tồn kho")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    image = models.ImageField(upload_to='books/', null=True, blank=True, default='books/default.jpg', verbose_name="Ảnh bìa")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="books",
        verbose_name="Danh mục",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sách"
        verbose_name_plural = "Sách"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Purchase(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name="Người dùng",
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name="Sách đã mua",
    )
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian mua")

    class Meta:
        verbose_name = "Lịch sử mua sách"
        verbose_name_plural = "Lịch sử mua sách"
        ordering = ["-purchased_at"]

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


class Wallet(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="wallet",
        verbose_name="Người dùng",
    )
    balance = models.BigIntegerField(default=0, verbose_name="Số dư (VNĐ)")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lúc")

    class Meta:
        verbose_name = "Ví người dùng"
        verbose_name_plural = "Ví người dùng"

    def __str__(self):
        return f"Ví của {self.user.username} ({self.balance:,} VNĐ)"


@receiver(post_save, sender=User)
def create_or_save_user_wallet(sender, instance, created, **kwargs):
    """Tự động tạo ví Wallet khi có User mới đăng ký."""
    if created:
        Wallet.objects.create(user=instance)
    else:
        if hasattr(instance, "wallet"):
            instance.wallet.save()

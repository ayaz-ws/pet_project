from django.db import models
import uuid

from django.contrib.auth.models import User


class Profile(models.Model):  # Создаем профиль для каждого User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    nickname = models.CharField(max_length=40, blank=True)
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        default="default-user-picture.webp",
    )
    location = models.CharField(max_length=100, blank=True)
    is_verify = models.BooleanField(verbose_name="Verifity", default=False)
    verify_uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    informate_about_views = models.CharField(
        verbose_name="Уведомлять о просмотрах по почте",
        max_length=5,
        choices=[("True", "Да"), ("False", "Нет")],
        default="False",
    )

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"

from django.contrib.auth import get_user_model
from django.db import models

from api.constants import (
    MAX_SLUG_LENGTH,
    MAX_TITLE_LENGTH,
    TEXT_PREVIEW_LENGTH,
)

User = get_user_model()


class Group(models.Model):
    """Модель сообществ (групп)."""

    title = models.CharField(
        max_length=MAX_TITLE_LENGTH,
        verbose_name="Заголовок",
    )
    slug = models.SlugField(
        max_length=MAX_SLUG_LENGTH,
        unique=True,
        verbose_name="Идентификатор (slug)",
    )
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.title[:TEXT_PREVIEW_LENGTH]


class Post(models.Model):
    """Модель публикаций (постов)."""

    text = models.TextField(verbose_name="Текст публикации")
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
    )
    image = models.ImageField(
        upload_to="posts/",
        null=True,
        blank=True,
        verbose_name="Изображение",
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="posts",
        verbose_name="Группа",
    )

    class Meta:
        ordering = ("pub_date",)
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"

    def __str__(self):
        return self.text[:TEXT_PREVIEW_LENGTH]


class Comment(models.Model):
    """Модель комментариев к публикациям."""

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Публикация",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    text = models.TextField(verbose_name="Текст комментария")
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="Дата создания",
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:TEXT_PREVIEW_LENGTH]


class Follow(models.Model):
    """Модель подписок пользователей."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "following"],
                name="unique_user_following",
            )
        ]

    def __str__(self):
        return f"{self.user.username} -> {self.following.username}"

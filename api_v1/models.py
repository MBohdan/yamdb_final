from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .utils import (current_year, max_value_current_year)


class Roles(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    bio = models.TextField(null=True, verbose_name='Информация о себе')
    confirmation_code = models.CharField(max_length=100, null=True,
                                         verbose_name='Код подтверждения',
                                         default=None)
    role = models.CharField(max_length=50, choices=Roles.choices,
                            verbose_name='Роль', default=Roles.USER)
    username = models.CharField(max_length=30, unique=True,
                                blank=True, null=True,
                                verbose_name='Псевдоним')
    email = models.EmailField(max_length=255, unique=True,
                              blank=False, null=False, verbose_name='Почта')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ["username"]

    @property
    def is_admin(self):
        return (self.is_staff
                or self.is_superuser
                or self.role == Roles.ADMIN)

    @property
    def is_moderator(self):
        return self.role == Roles.MODERATOR

    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название жанра")
    slug = models.SlugField(unique=True, verbose_name="Slug жанра")

    class Meta:
        ordering = ["name"]
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название категории")
    slug = models.SlugField(unique=True, verbose_name="Slug категории")

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Title(models.Model):
    name = models.CharField(
        max_length=200, blank=False, verbose_name="Название произведения"
    )

    year = models.PositiveIntegerField(
        default=current_year(),
        validators=[max_value_current_year],
        verbose_name="Год выхода",
        db_index=True,
    )
    description = models.TextField(
        null=True, blank=True, verbose_name="Описание"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        blank=True,
        null=True,
        verbose_name="Категория",
    )
    genre = models.ManyToManyField(
        Genre, related_name="titles", verbose_name="Жанр"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name='произведение',
    )
    text = models.TextField(
        verbose_name='тексты отзыва',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name='автор отзыва',
    )
    score = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=False,
        null=False,
        verbose_name='оценка произведения',
    )
    pub_date = models.DateTimeField(
        "review date published",
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        unique_together = ['author', 'title']
        ordering = ["pub_date"]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв от {self.author} на {self.title}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name="comments",
        verbose_name='отзыв',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="comments",
        verbose_name='автор комментария',
    )
    text = models.TextField(
        verbose_name='текст комментария',
    )
    pub_date = models.DateTimeField(
        "comment date published",
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ["pub_date"]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.author} к {self.review}'

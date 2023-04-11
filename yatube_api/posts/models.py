from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название Группы',
        default='-пусто-',
        help_text='Напишите, как будет называться группа'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Уникальный адрес для страницы с группой'
    )
    description = models.TextField(
        verbose_name='Описание Группы',
        help_text='Кратко опишите, о чем будет группа'
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Напишите, о чем сейчас думаете'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        help_text='Тут указывается автор поста',
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Группа',
        help_text='Создавайте группы по интересам'
    )

    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        null=True,
        blank=True
    )

    class Meta:
        default_related_name = 'posts'
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор коммента',
        help_text='Тут указывается автор коммента'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Запись',
        help_text='Напишите, о чем сейчас думаете'
    )
    text = models.TextField(
        verbose_name='Текст коммента',
        help_text='Напишите, о чем сейчас думаете'
    )
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        default_related_name = 'comments'
        ordering = ('-created',)
        verbose_name = 'Коммент'
        verbose_name_plural = 'Комменты'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Кто Подписывается',
        help_text='Тут указывается кто подписывается',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='На кого подписывается',
        help_text='Тут указывается на кого подписывается'
    )
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Избранный автор'
        verbose_name_plural = 'Избранные авторы'

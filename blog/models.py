from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    name = models.CharField('nome', max_length=100, unique=True)
    description = models.TextField('descrição', blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'categoria'
        verbose_name_plural = 'categorias'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_detail', kwargs={'pk': self.pk})


class Post(models.Model):
    title = models.CharField('título', max_length=200)
    content = models.TextField('conteúdo (HTML)')
    posted_at = models.DateTimeField('data de postagem', default=timezone.now)
    categories = models.ManyToManyField(
        Category, related_name='posts', blank=True, verbose_name='categorias'
    )

    class Meta:
        ordering = ['-posted_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments', verbose_name='post'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='autor'
    )
    text = models.TextField('texto')
    posted_at = models.DateTimeField('data de postagem', default=timezone.now)

    class Meta:
        ordering = ['-posted_at']

    def __str__(self):
        return f'{self.author} em "{self.post}"'

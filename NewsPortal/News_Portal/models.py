from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        comment_rating = Comment.objects.filter(user=self.user).aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        posts_com_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Coalesce(Sum('rating'), 0))['pcr']

        self.rating = posts_rating * 3 + posts_com_rating + comment_rating
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    sport = 'SP'
    politics = 'PO'
    education = 'ED'
    science = 'SC'

    CHAPTER = [
        (sport, 'Спорт'),
        (politics, 'Политика'),
        (education, 'Образование'),
        (science, 'Наука'),
    ]

    themes = models.CharField(max_length=2, choices=CHAPTER, default=sport, unique=True)

    def __str__(self):
        return self.themes.title()


class Post(models.Model):

    article = 'A'
    news = 'N'

    CHOICE = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]
    authors = models.ForeignKey(Author, on_delete=models.CASCADE)
    selection_field = models.CharField(max_length=1, choices=CHOICE, default=news)
    time_of_publication = models.DateTimeField(auto_now_add=True)
    section = models.ManyToManyField(Category, through='PostCategory')
    header_post = models.CharField(max_length=100)
    text_post = models.TextField(default='Не заполнено')
    rating = models.IntegerField(default=0)

    def preview(self):
        return self.text_post[:125] + '...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"{self.header_post.title()}: {self.text_post[:20]}"

    def get_absolute_url(self):
        return reverse('new', args=[str(self.id)])

class PostCategory(models.Model):
    Posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    Categories = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_com = models.TextField(default='Нет комментариев')
    time_com = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

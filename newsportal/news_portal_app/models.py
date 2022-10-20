from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        # return self.commentPost.author.authorUser.username  # получить имя автора поста
        return f'{self.user.username}'

    def update_ratings(self):
        posts_rating = self.post_set.aggregate(result=Sum('rating')).get('result')
        comments_rating = self.user.comment_set.aggregate(result=Sum('rating')).get('result')
        print(f"===== {self.user}: обновляем рейтинг автора =====")
        print(f"Рейтинг постов = {posts_rating}")
        print(f"Рейтинг комментов = {comments_rating}")
        self.rating = 3 * posts_rating + comments_rating
        self.save()
        print(f"Рейтинг = 3 * {posts_rating} + {comments_rating} = {self.rating}")


class Category(models.Model):
    name_category = models.CharField(max_length=128, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscriber', blank=True)

    def __str__(self):
        return f'{self.name_category}'


class Post(models.Model):
    news = 'NE'
    artikle = 'AR'

    TYPE = [
        (news, 'Новость'),
        (artikle, 'Статья'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPE, default=artikle)
    time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self, length=124):
        return f"{self.text[:length]}..." if len(str(self.text)) > length else self.text

    def get_absolute_url(self):
        """ Вернуть url, зарегистрированный для отображения одиночного товара """
        return reverse('post_detail', args=[str(self.id)])

    def __str__(self):
        # получить название поста
        return f'{self.title}. {self.text[:124]} ...'

    def get_category(self):
        return f'{self.category}'

    def message_subscriber(self):
        return f'Новая статья - "{self.title}" в разделе "{self.category.first()}" '


class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        # получить название поста
        return f'{self.post}. {self.category}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating = + 1
        self.save()

    def dislike(self):
        self.rating = - 1
        self.save()

    def __str__(self):
        # return self.commentPost.author.authorUser.username  # получить имя автора поста
        return f'{self.user.username}'
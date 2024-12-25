import datetime

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.user.username



class Tag(models.Model):
    name = models.CharField(max_length=50)
    questions_num = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updeted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class QuestionManager(models.Manager):
    def get_newest(self):
        return self.order_by('-created_at')

    def get_hottest(self):
        return self.order_by('likes_num')

    def get_by_tag(self, need_tag):
        return self.filter(tag_name_exact=need_tag)


class Question(models.Model):
    objects = QuestionManager()

    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    title = models.CharField(max_length=255)
    text = models.TextField(max_length=1000)
    likes_num = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updeted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_created_at(self):
        return self.created_at

    def get_tags(self):
        return [el for el in self.tag.name]


class AnswerManager(models.Manager):
    def get_answers(self, question_id):
        return self.filter(question_id__exact=question_id)

    def get_answers_num(self, question_id):
        return len(self.filter(question_id__exact=question_id))


class Answer(models.Model):
    objects = AnswerManager()
    STATUS_CHOICES = [
        ('c', 'Correct'),
        ('nc', 'Not Correct')
    ]
    correct_status = models.CharField(choices=STATUS_CHOICES, max_length=30)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    text = models.TextField(max_length=1000)
    likes_num = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updeted_at = models.DateTimeField(auto_now=True)


class QuesLikeManager(models.Manager):
    def get_likes_num(self, question_id):
        return len(self.filter(question_id__exact=question_id))

class QuestionLike(models.Model):
    objects = QuesLikeManager()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updeted_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('profile', 'question')


class AnswerLike(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updeted_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('profile', 'answer')

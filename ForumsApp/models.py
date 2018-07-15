from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Questions(models.Model):
    title=models.CharField(max_length=64)
    description = models.TextField(max_length=1024)
    tags=models.CharField(max_length=32)
    username=models.ForeignKey(User,on_delete=models.CASCADE)


class Answers(models.Model):
    description = models.TextField()
    likes=models.IntegerField(default=0)
    dislikes=models.IntegerField(default=0)
    question=models.ForeignKey(Questions,on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)


class AnswersComments(models.Model):
    description = models.TextField()
    answer=models.ForeignKey(Answers,on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

class QuestionsComments(models.Model):
    description = models.TextField()
    answer=models.ForeignKey(Answers,on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

class AnswerVotes(models.Model):
    vote=models.IntegerField(default=0)
    answer=models.ForeignKey(Answers,on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)




# title and description can have null and blank attributes
# for smaller strings use CharField
# for larger strings use TextField
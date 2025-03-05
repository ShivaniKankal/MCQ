from django.db import models
import random
from django.contrib.auth.models import User


class Question(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

    @staticmethod
    def get_random_questions(count=10):
        return list(Question.objects.order_by("?")[:count])


class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class TestSession(models.Model):
    session_id = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional
    created_at = models.DateTimeField(auto_now_add=True)


class UserResponse(models.Model):
    test_session = models.ForeignKey(TestSession, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def is_correct(self):
        return self.selected_choice.is_correct

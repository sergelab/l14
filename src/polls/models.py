from django.db import models


class Question(models.Model):
    title = models.CharField(max_length=4096)
    visible = models.BooleanField()
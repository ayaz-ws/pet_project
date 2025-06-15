from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-created",)

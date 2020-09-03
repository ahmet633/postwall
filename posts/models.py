from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Post(models.Model):
    # QUESTION: user silindiğinde postları ne olacak
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='post_user', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


    class Meta:
        ordering = ['-id']

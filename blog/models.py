from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Post Model
class Post(models.Model):
    # add fields you want to add
    title = models.CharField(max_length=100)
    content = models.TextField()
    # (auto_now=True) (auto_now_add=True) - caveat both can no longer change the data
    date_posted = models.DateTimeField(default=timezone.now)
    # if the USER is deleted - delete all the Posts as well. 1 way, User to post only
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # tell Django how to find the URL in any specific instance of a post
    # Setting for after PostCreateView, Django redirects to here
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})



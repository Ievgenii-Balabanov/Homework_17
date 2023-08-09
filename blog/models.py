from django.db import models
from django.contrib.auth.models import AbstractUser

from django.urls import reverse


class MyUser(AbstractUser):
    about = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images")


STATUS = ((0, "Draft"), (1, "Publish"))


class UserPost(models.Model):
    title = models.CharField(max_length=200, unique=True)
    summary = models.CharField(max_length=100)
    image = models.ImageField(upload_to="media/images", blank=True, null=True)
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="blog_posts")
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_on"]
        permissions = (("can_update_post", "Can update some own posts"),)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        some_id = self.pk
        return reverse("blog:post_detail", kwargs={"pk": some_id})


class Comment(models.Model):
    name = models.CharField(max_length=70)
    body = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name="comments")

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return "Comment {} by {}".format(self.body, self.name)

from django.db import models

class GithubUser(models.Model):
    login = models.CharField(max_length=50)
    language = models.CharField(max_length=30, blank=True, null=True)
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=80, blank=True, null=True)
    fullname  = models.CharField(max_length=80, blank=True, null=True)
    location = models.CharField(max_length=80)
    public_repo_count = models.IntegerField()
    created = models.DateTimeField()
    repos = models.IntegerField()
    github_id = models.CharField(max_length=20, unique=True)
    followers = models.IntegerField()
    score = models.FloatField()
    gravatar_id = models.CharField(max_length=40, blank=True, null=True)

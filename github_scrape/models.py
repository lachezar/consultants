from django.db import models

class GithubUser(models.Model):
    login = models.CharField(max_length=50)
    language = models.CharField(max_length=30)
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=80)
    fullname  = models.CharField(max_length=80)
    location = models.CharField(max_length=80)
    public_repo_count = models.IntegerField()
    created = models.DateTimeField()
    repos = models.IntegerField()
    github_id = models.CharField(max_length=20, unique=True)
    followers = models.IntegerField()
    score = models.FloatField()

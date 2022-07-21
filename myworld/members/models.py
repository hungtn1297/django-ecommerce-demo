from django.db import models


class Members(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)


class Books(models.Model):
    name = models.CharField(max_length=255)
    code = models.BigIntegerField()

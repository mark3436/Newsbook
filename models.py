from django.db import models

# Create your models here.
class Publishers(models.Model):
    name = models.CharField(max_length=250)
    logo = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000)
    def __str__(self):
        return self.name
class Newss(models.Model):
    publisher = models.ForeignKey(Publishers, on_delete=models.CASCADE)
    title = models.CharField(max_length=250, null = True)
    topic = models.CharField(max_length=25, null = True)
    reference_id = models.CharField(max_length=50, null = True)
    body = models.TextField(max_length = 25000, null = True)
    image_url = models.CharField(max_length = 1000, null = True)
    datetime = models.DateTimeField(null = True)
    #image_urls = models.CharField(max_length = 1000)
    #datetimes = models.CharField(max_length = 200)
    def __str__(self):
        return self.title + ' - ' + self.topic
class user(models.Model):
    name = models.CharField(max_length=250)
class Tags(models.Model):
    tagname = models.CharField(max_length=100)

class News_tags(models.Model):
    newsid = models.ForeignKey(Newss, on_delete=models.CASCADE)
    tagid = models.ForeignKey(Tags, on_delete=models.CASCADE)

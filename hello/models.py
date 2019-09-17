from django.db import models
from django.utils import timezone

# Create your models here.
class URLCollection(models.Model):
    URL= models.TextField()
    email= models.TextField()
    price= models.IntegerField()
    date_added = models.DateTimeField(default=timezone.now)
    sendMail= models.BooleanField(default=False)

    def __str__(self):
        return '<Name: {}, ID: {}>'.format(self.email, self.id)
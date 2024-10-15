from django.db import models
from django.contrib.auth.models import User

class Bookmark(models.Model):
    url = models.URLField(max_length=200)
    title = models.CharField(max_length=100)
    

    def __str__(self):
        return self.title
    



    


    

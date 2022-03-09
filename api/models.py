from django.db import models

# Create your models here.
class users(models.Model):
    user_name=models.CharField(max_length=200,null=False,blank=False)
    tocken = models.CharField(max_length=200,null=False,blank=False)
    def __str__(self):
        return self.user_name
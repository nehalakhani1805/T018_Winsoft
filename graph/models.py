from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Input(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    enc_string = models.CharField(max_length=100)

    #def __str__(self):
        #return self.key+ '|'+ self.user

class Vertex(models.Model):
    code=models.CharField(max_length=2)
    name=models.CharField(max_length=100)
    x_val=models.IntegerField()
    y_val=models.IntegerField()

    def __str__(self):
        return self.code
    class Meta:
        verbose_name_plural = "Vertices"


class Edge(models.Model):
    v_one = models.ForeignKey('Vertex',on_delete=models.CASCADE, null=True, related_name='vertexone')
    v_two = models.ForeignKey('Vertex',on_delete=models.CASCADE,null=True, related_name='vertextwo')
    diff = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.v_one) + '-'+ str(self.v_two)


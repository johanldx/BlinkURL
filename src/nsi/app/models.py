from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Url(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(verbose_name='Créé le', default=timezone.now())
    name = models.CharField(max_length=100, verbose_name='Nom', default=None)
    url = models.CharField(max_length=250, verbose_name='URL', default=None)
    key = models.CharField(max_length=250, verbose_name='URL raccourcis', default=None)
    statistics = models.IntegerField(verbose_name='Nombre de cliques', default=0)
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE, verbose_name="Utilisateur")

    def __str__(self):
        return f"{self.name} ({self.user.username})"

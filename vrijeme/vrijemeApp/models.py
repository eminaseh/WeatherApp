from djongo import models
from django.contrib.auth.models import User

# Create your models here.
class Grad(models.Model):
    naziv = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.naziv

    class Meta:
        verbose_name_plural = 'gradovi'


class Korisnik(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    grad_naziv = models.CharField(max_length=30, null=True)
    ime = models.CharField(max_length=30, null=True)
    email = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.ime

    class Meta:
        verbose_name_plural = 'korisnici'


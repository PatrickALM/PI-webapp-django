from django.db import models
import datetime 

# Create your models here.
class Usuariosdb(models.Model):
    nome = models.CharField(max_length=30)
    sobrenome = models.CharField(max_length=30)
    endereco = models.CharField(max_length=100)
    telefone = models.CharField(max_length=30)
    matricula =  models.CharField(max_length=30)
    data_cadastro = models.DateField(default=datetime.date.today)
    email = models.EmailField(max_length=30, default=None, null=True)              

    class Meta:
        verbose_name = 'Usuário'

    def __str__(self):
        return self.nome + ' ' + self.sobrenome


class Funcionariosdb(models.Model):
    nome = models.CharField(max_length=30)
    sobrenome = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    senha = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'Funcionário'

    def __str__(self):
        return self.nome + ' ' + self.sobrenome
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
from usuarios.models import Usuariosdb,Funcionariosdb


class Categoriadb(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome

class Livrosdb(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=50)
    disponibilidade = models.BooleanField(default=True)
    img_livro = models.BinaryField(blank=True, null=True, default=None)
    ISBN = models.CharField(max_length=100)
    data_cadastro = models.DateField(default=datetime.date.today)
    ano_de_publicacao = models.PositiveIntegerField(default=datetime.date.today().year,
            validators=[
                MinValueValidator(1900), 
                MaxValueValidator(datetime.date.today().year)])
    categoria = models.ForeignKey(Categoriadb,on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Livro'

    def __str__(self):
        return self.titulo



class Emprestimosdb(models.Model):
    id_livro = models.ForeignKey(Livrosdb, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuariosdb, on_delete=models.CASCADE)
    id_funcionario = models.ForeignKey(Funcionariosdb, on_delete=models.CASCADE)
    data_saida = models.DateField(default=datetime.date.today())
    data_retorno = models.DateField()
    situacao = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Empréstimo'

    def __str__(self):
        return self.data_saida + ' - ' + self.data_retorno


    


'''
TABELA USUARIO

ID
NOME
SOBRENOME
ENDERECO
NUMERO
matriculo


TABELA FUNCIONARIO
ID
NOME
SOBRENOME
EMAIL
SENHA

TABELA EMPRESTIMO
ID_EMPRESTIMO
ID_LIVRO
ID_USUARIO
DATA_SAIDA
DATA_RETORNO
SITUAÇÃO
ID_FUNCIONARIO

'''
    


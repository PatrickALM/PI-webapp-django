from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
import datetime
from usuarios.models import Usuariosdb,Funcionariosdb

situacoes = (
    ('Em andamento','Em andamento'),
    ('Atrasado','Atrasado'),
    ('Concluido','Concluido'),
)




class Categoriadb(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome

class Livrosdb(models.Model):
    img = models.ImageField(upload_to='capa_livro', null=True, blank=True)
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=50)
    disponibilidade = models.BooleanField(default=True)
    img_livro = models.BinaryField(blank=True, null=True, default=None)
    ISBN = models.CharField(max_length=13,validators=[MinLengthValidator(13,'Certifique-se de digitar um ISBN válido')])
    data_cadastro = models.DateField(default=datetime.date.today())
    ano_de_publicacao = models.PositiveIntegerField(default=datetime.date.today().year,
            validators=[
                MinValueValidator(1900,'Certifique-se que o ano de publicação seja maior ou igual a 1900.'), 
                MaxValueValidator(datetime.date.today().year,'Certifique-se de que o ano de publicação seja uma data válida')])
    unidades = models.IntegerField(default=1, validators=[MinValueValidator(1,'Certifique-se de que a quantidade de exemplares seja maior ou igual a 1')])
    qntd_emprestado =  models.IntegerField(default=0)

    categoria = models.ForeignKey(Categoriadb,on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Livro'

    def __str__(self):
        return self.titulo



class Emprestimosdb(models.Model):
    id_livro = models.ForeignKey(Livrosdb, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Usuariosdb, on_delete=models.CASCADE)
    id_funcionario = models.ForeignKey(Funcionariosdb, on_delete=models.CASCADE, null=True, default=None)
    data_saida = models.DateField(default=datetime.date.today())
    data_retorno_previsto = models.DateField(default=datetime.date.today() + datetime.timedelta(days=7))
    data_retorno = models.DateField(null=True,blank=True,default=None)
    situacao = models.CharField(max_length=30, choices=situacoes, default='Em andamento')

    class Meta:
        verbose_name = 'Empréstimo'
    
    def __str__(self):
        return  self.id_usuario.nome + ' ' + self.id_usuario.sobrenome + ' || ' + 'Livro:' + self.id_livro.titulo + ' ||  Retorno:' + self.data_retorno_previsto.strftime("%d/%m/%Y")   + ' ||  Status: ' + self.situacao



    
    


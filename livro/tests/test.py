from django.test import TestCase
from livro.models import Categoriadb, Livrosdb, Emprestimosdb
from usuarios.models import Usuariosdb, Funcionariosdb
import datetime

# Teste da Model.

class LivroTestModel(TestCase):

    def test_model_categoriadb(self):
        nome = Categoriadb.objects.create(nome="Tecnologia")
        self.assertEqual(str(nome),"Tecnologia")


    def test_model_livrosdb(self):

        categoria = Categoriadb.objects.create(nome="Tecnologia")

        titulo = Livrosdb.objects.create(
            titulo="Titulo do livro",
            autor="Autor do livro", 
            ISBN="1234567891234", 
            ano_de_publicacao="2020",
            unidades="2", 
            categoria=categoria )
        self.assertEqual(str(titulo),"Titulo do livro")

    def test_model_emprestimodb(self):
        categoria = Categoriadb.objects.create(nome="Tecnologia")

        livro =  Livrosdb.objects.create(
                titulo="Titulo do livro",
                autor="Autor do livro", 
                ISBN="1234567891234", 
                ano_de_publicacao="2020",
                unidades="2", 
                categoria=categoria 
        )  
        usuario = Usuariosdb.objects.create(
            nome="Nome",
            sobrenome="Sobrenome",
            endereco="Endereço",
            telefone="11999999999",
            matricula="123456"
        )
        funcionario = Funcionariosdb.objects.create(
            nome="Nome",
            sobrenome="Sobrenome",
            email="email@email.com.br",
            senha="1234"
        )
        
        emprestimo = Emprestimosdb.objects.create(
            id_livro=livro,
            id_usuario=usuario,
            id_funcionario=funcionario,
            data_saida=datetime.date.today(),
            data_retorno_previsto=datetime.date.today() + datetime.timedelta(days=7),
            situacao="Em andamento"
            )
        self.assertEqual(str(emprestimo),f"{usuario.nome} {usuario.sobrenome} || Livro:{livro.titulo} ||  Retorno:{emprestimo.data_retorno_previsto.strftime('%d/%m/%Y')} ||  Status: Em andamento")     

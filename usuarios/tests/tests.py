from django.test import TestCase
from usuarios.models import Usuariosdb, Funcionariosdb

# Testes das models de usuario
class UsuariosTestModel(TestCase):
    def test_model_usuariosdb(self):
        usuario = Usuariosdb.objects.create(
            nome="Nome",
            sobrenome="Sobrenome",
            endereco="Endereço",
            telefone="11999999999",
            matricula="123456"
        )

        self.assertEqual(str(usuario),"Nome Sobrenome")

    def teste_model_funcionariodb(self):
        funcionario = Funcionariosdb.objects.create(
            nome="Nome",
            sobrenome="Sobrenome",
            email="email@email.com.br",
            senha="1234"
        )
        self.assertEqual(str(funcionario),"Nome Sobrenome")
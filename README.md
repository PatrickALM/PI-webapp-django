# :pushpin: Projeto Integrador: 2° Semestre 2023 

Trata-se de uma atividade curricular obrigatória, que consiste na resolução de um problema real contextualizado na area de Computação,a fim de que seja possível elaborar possibilidades de soluções para problemas existentes na sociedade.

#### Tema norteador​: 
Desenvolver um software com framework web que utilize banco de dados, inclua script web (Javascript), nuvem, uso de API, acessibilidade, controle de versão e testes. Opcionalmente, incluir análise de dados.

#### Resumo

-----------

#### Instruções para rodar o protótipo 


1. Acesse o diretório do repositório em seu computador

2. Ative o ambiente virtual

No Windows
~~~
pi2-venv\Scripts\activate.bat
~~~

No Linux
~~~
source pi2-venv\Scripts\activate
~~~ 

3. Atualize as configurações do banco de dados

~~~
python manage.py makemigrations
~~~ 

~~~
python manage.py migrate
~~~ 

4. Crie o superusuário para conseguir acessar a pagina de administração do django e popular as tabelas com os dados

~~~
python manage.py createsuperuser 
~~~ 


5. Inicie o servidor web
~~~
python manage.py runserver
~~~

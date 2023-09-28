from django.contrib import admin
from .models import Livrosdb, Categoriadb,Emprestimosdb

admin.site.register(Livrosdb)
admin.site.register(Categoriadb)
admin.site.register(Emprestimosdb)
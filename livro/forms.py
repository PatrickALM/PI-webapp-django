from django import forms
from .models import Livrosdb, Categoriadb

CATEGORIA_FILTRO =[
    ("0", "Todas"),
    ("1", "Física"),
    ("2", "Química"),
    ("3", "Biologia"),
    ("4", "Matemática"),
    ("5", "Engenharia"),
    ("6", "Historia"),
    ("7", "Geografia"),
    ("8", "Economia"),
    ("9", "Sociologia"),
    ("10", "Artes"),
    ("11", "Tecnologia"),
    ("12", "Ficção"),
]

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livrosdb
        fields = ('titulo','autor','ISBN','ano_de_publicacao','categoria')

class FiltroCategoria(forms.Form):
    categoria = forms.ChoiceField(choices=CATEGORIA_FILTRO,widget=forms.Select(attrs={'onchange': 'filtro_categoria.submit();'}))

from django import forms
from .models import Livrosdb

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

DISP_FILTRO = [
    ("0", "Todos"),
    ("1", "Disponíveis"),
    ("2", "Não disponíveis")
    
]

ORDER_BY = [
    ("0", "Mais recentes"),
    ("1", "Mais antigos"),
    ("2", "A-z"),
    ("3", "Z-a")
    
]

class LivroForm(forms.ModelForm):
    class Meta:
        model = Livrosdb
        fields = ('titulo','autor','ISBN','ano_de_publicacao','categoria')

    
    def __init__(self, *args, **kwargs):
        super(LivroForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control my-2 ms-2'

class FiltroForm(forms.Form):
    categoria = forms.ChoiceField(choices=CATEGORIA_FILTRO,widget=forms.Select(attrs={'onchange': 'filtro.submit();'}))
    disponibilidade = forms.ChoiceField(choices=DISP_FILTRO,widget=forms.Select(attrs={'onchange': 'filtro.submit();'}))
    order = forms.ChoiceField(choices=ORDER_BY,widget=forms.Select(attrs={'onchange': 'filtro.submit();'}))

    def __init__(self, *args, **kwargs):
        super(FiltroForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-select'
    

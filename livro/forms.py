from django import forms
from .models import Livrosdb, Emprestimosdb

CATEGORIA_FILTRO =[
    ("0", "Todos"),
    ("4", "Biografia"),
    ("5", "Escolar"),
    ("6", "Engenharia"),
    ("7", "Economia"),
    ("8", "Ficcao"),
    ("9", "Filosofia"),
    ("10", "Saude"),
    ("11", "Tecnologia"),
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
        fields = ('titulo','autor','ISBN','ano_de_publicacao','categoria','img')

    
    def __init__(self, *args, **kwargs):
        super(LivroForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control my-2 ms-2'

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimosdb
        fields = ('id_livro','id_usuario','data_saida','data_retorno_previsto')

    
    def __init__(self, *args, **kwargs):
        super(EmprestimoForm, self).__init__(*args, **kwargs)
        
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
    

from django import forms
from .models import Livrosdb, Emprestimosdb,Usuariosdb
from django.core.exceptions import ValidationError


TUPLA_TODOS = (0,"Todos")

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

STATUS_FILTRO = [
    ("0", "Todos"),
    ("1", 'Em andamento'),
    ("2", 'Atrasado'),
    ("3",'Concluido'), 
]

ORDER_BY = [
    ("0", "Mais recentes"),
    ("1", "Mais antigos"),
    ("2", "A-z"),
    ("3", "Z-a")
    
]
NOME_FILTRO = [(0,"Todos"),]
for i in Usuariosdb.objects.all():
    NOME_FILTRO.append((i.id, i.__str__))

# LIVRO_FILTRO = [(0,"Todos"),]
LIVRO_FILTRO = list(Livrosdb.objects.values_list('id','titulo'))
LIVRO_FILTRO.insert(0,TUPLA_TODOS)


class LivroForm(forms.ModelForm):
    class Meta:
        model = Livrosdb
        fields = ('titulo','autor','ISBN','ano_de_publicacao','categoria','unidades','img')

    
    def __init__(self, *args, **kwargs):
        super(LivroForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control my-2 ms-2'

        

class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimosdb
        fields = ('id_livro','id_usuario','data_saida','data_retorno_previsto')
        labels = {
            'id_livro': 'Livros Disponíveis',
            'id_usuario': 'Usuário'
        }

    
    def __init__(self,*args, **kwargs):
        super(EmprestimoForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control my-4 ms-4'
            
        
        self.fields['id_livro'].queryset = Livrosdb.objects.filter(disponibilidade=True).order_by('titulo')
        self.fields['id_usuario'].queryset = Usuariosdb.objects.all().order_by('nome')

        
        self.fields['id_livro'].widget.attrs['class'] ="form-control border my-4 ms-4 selectpicker"
        self.fields['id_livro'].widget.attrs['data-live-search'] = "true"
        self.fields['id_livro'].widget.attrs['data-live-search-style'] = "startsWith"

        self.fields['id_usuario'].widget.attrs['class'] ="form-control border my-4 ms-4 selectpicker"
        self.fields['id_usuario'].widget.attrs['data-live-search'] = "true"
        self.fields['id_usuario'].widget.attrs['data-live-search-style'] = "startsWith"
        
        



class FiltroForm(forms.Form):
    categoria = forms.ChoiceField(choices=CATEGORIA_FILTRO,widget=forms.Select(attrs={'onchange': 'filtro.submit();'}))
    disponibilidade = forms.ChoiceField(choices=DISP_FILTRO,widget=forms.Select(attrs={'onchange': 'filtro.submit();'}))
    order = forms.ChoiceField(choices=ORDER_BY,widget=forms.Select(attrs={'onchange': 'filtro.submit();'}))

    def __init__(self, *args, **kwargs):
        super(FiltroForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-select'


class FiltroEmprestimoForm(forms.Form):
    nome = forms.ChoiceField(choices=NOME_FILTRO,widget=forms.Select(attrs={'onchange': 'filtro.submit();'}))
    livro = forms.ChoiceField(choices=LIVRO_FILTRO,widget=forms.Select(attrs={'onchange': 'filtro.submit();'}))
    situacao = forms.ChoiceField(choices=STATUS_FILTRO,widget=forms.Select(attrs={'onchange': 'filtro.submit();'}))
    order = forms.ChoiceField(choices=ORDER_BY[0:2],widget=forms.Select(attrs={'onchange': 'filtro.submit();'}))

    def __init__(self, *args, **kwargs):
        super(FiltroEmprestimoForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-select'

        self.fields['nome'].widget.attrs['class'] ="form-control border selectpicker"
        self.fields['nome'].widget.attrs['data-live-search'] = "true"
        self.fields['nome'].widget.attrs['data-live-search-style'] = "startsWith"

        self.fields['livro'].widget.attrs['class'] ="form-control border selectpicker"
        self.fields['livro'].widget.attrs['data-live-search'] = "true"
        self.fields['livro'].widget.attrs['data-live-search-style'] = "startsWith"

        self.fields['situacao'].widget.attrs['class'] ="form-control border selectpicker"

        self.fields['order'].widget.attrs['class'] ="form-control border selectpicker"



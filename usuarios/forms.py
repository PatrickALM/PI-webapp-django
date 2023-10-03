from django import forms
from .models import Usuariosdb

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuariosdb
        fields = ('nome','sobrenome','endereco','telefone','matricula')

    
    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control my-2 ms-2'
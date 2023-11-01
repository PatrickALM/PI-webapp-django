import datetime
import pandas as pd
from livro.models import  Emprestimosdb


def update_status_emprestimo():
    emps = Emprestimosdb.objects.all()

    for row in emps:
        if (pd.to_datetime(row.data_retorno_previsto) < pd.Timestamp(datetime.date.today())) and (row.situacao == 'Em andamento'):
            row.situacao = 'Atrasado'
            row.save()
    
    
    return


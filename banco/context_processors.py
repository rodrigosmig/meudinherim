from banco.models import ContaBanco
from caixa.models import Categoria

def transferencia_bancaria(request):
    if(request.user.is_authenticated):
        agencias = ContaBanco.getAgencias(request.user)
        categoriasEntrada = Categoria.getCategorias(request.user, Categoria.ENTRADA)
        categoriasSaida = Categoria.getCategorias(request.user, Categoria.SAIDA)
        
        contexto = {
            'lista_agencias': agencias,
            'lista_categoria_entrada': categoriasEntrada,
            'lista_categoria_saida': categoriasSaida
        }

        return contexto
    
    return {'lista_agencias': []}
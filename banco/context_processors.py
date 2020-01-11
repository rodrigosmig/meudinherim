from banco.models import ContaBanco
from caixa.models import Categoria

def agencias(request):
    if(request.user.is_authenticated):
        agencias = ContaBanco.getAgencias(request.user)
        categoriasEntrada = Categoria.getCategorias(request.user, Categoria.ENTRADA)
        categoriasSaida = Categoria.getCategorias(request.user, Categoria.SAIDA)
        
        contexto = {
            'agencias_transferencias': agencias,
            'categoria_entrada_transferencia': categoriasEntrada,
            'categoria_saida_transferencia': categoriasSaida
        }

        return contexto
    
    return {'agencias_transferencias': []}
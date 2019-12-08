from rest_framework import serializers
from caixa.models import Categoria, LancamentosCaixa
from contas_a_pagar.api.serializers import ContasAPagarSerializer
from contas_a_receber.api.serializers import ContasAReceberSerializer

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Categoria
        fields  = ('id', 'descricao', 'tipo', 'user')
        related_fields = ['user']

class LancamentosCaixaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LancamentosCaixa
        fields = (
            'id', 
            'data', 
            'categoria', 
            'descricao', 
            'valor', 
            'conta_a_pagar', 
            'conta_a_receber', 
            'user'
        )
from rest_framework import serializers
from banco.models import ContaBanco, LancamentosBanco

class ContaBancoSerializer(serializers.ModelSerializer):
    class Meta:
        model           = ContaBanco
        fields          = ('id', 'banco', 'agencia', 'conta', "tipo", 'dia_fechamento', 'limite', 'saldo', 'user')
        related_fields  = ['user']

class LancamentosBancoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LancamentosBanco
        fields = (
            'id',
            'banco',
            'data', 
            'categoria',
            'tipo',
            'descricao', 
            'valor',
            'conta_a_pagar', 
            'conta_a_receber', 
            'user'
        )

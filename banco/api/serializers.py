from rest_framework import serializers
from banco.models import ContaBanco

class ContaBancoSerializer(serializers.ModelSerializer):
    class Meta:
        model           = ContaBanco
        fields          = ('id', 'banco', 'agencia', 'conta', "tipo", 'dia_fechamento', 'limite', 'saldo', 'user')
        related_fields  = ['user']
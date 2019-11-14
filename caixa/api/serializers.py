from rest_framework import serializers
from caixa.models import Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    #tipo = serializers.CharField(source='get_tipo_display')
    class Meta:
        model = Categoria
        fields = ('id', 'descricao', 'tipo', 'user')
        related_fields = ['user']
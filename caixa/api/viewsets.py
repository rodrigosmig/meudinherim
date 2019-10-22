from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from caixa.models import Categoria
from usuario.models import UsuarioProfile
from django.contrib.auth.models import User
from .serializers import CategoriaSerializer
from rest_framework import status

class CategoriaViewSet(ModelViewSet):
    serializer_class = CategoriaSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        return Categoria.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):        
        return super(CategoriaViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if 'user' in request.data:
            try:
                user = User.objects.get(pk = request.data['user'])
            except User.DoesNotExist as erro:
                return Response({"user": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

            if user != request.user:
                return Response({'user': "Não é possível criar categorias para outro usuário."}, status=status.HTTP_403_FORBIDDEN)
        
        return super(CategoriaViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        msg = {
            "message: Categoria " + instance.descricao + " excluída com sucesso"
            }
        return Response(msg, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        return super(CategoriaViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if 'user' in request.data:
            try:
                user = User.objects.get(pk = request.data['user'])
            except User.DoesNotExist as erro:
                return Response({"user": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

            if user != request.user:
                return Response({'user': "Não é possível atribuir categorias para outro usuário."}, status=status.HTTP_403_FORBIDDEN)

        return super(CategoriaViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):        
        return super(CategoriaViewSet, self).partial_update(request, *args, **kwargs)
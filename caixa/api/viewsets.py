from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from caixa.models import Categoria, LancamentosCaixa
from django.contrib.auth.models import User
from .serializers import CategoriaSerializer, LancamentosCaixaSerializer
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


class LancamentosCaixaViewSet(ModelViewSet):
    serializer_class = LancamentosCaixaSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        return LancamentosCaixa.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        user = request.user
        if 'user' in request.data:
            try:
                user_request = User.objects.get(pk = request.data['user'])
            except User.DoesNotExist as erro:
                return Response({"user": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

            if user_request != user:
                return Response({'user': "Usuário inválido."}, status=status.HTTP_403_FORBIDDEN)
        
        if 'categoria' in request.data:
            try:
                categoria = Categoria.objects.get(pk=request.data['categoria'])
            except Categoria.DoesNotExist as identifier:
                return Response({"categoria": "Categoria não encontrada."}, status=status.HTTP_404_NOT_FOUND)
            if categoria.user != user:
                return Response({"categoria": "Categoria não encontrada."}, status=status.HTTP_404_NOT_FOUND)
        
        return super(LancamentosCaixaViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        msg = {
            "message: Categoria " + instance.descricao + " excluída com sucesso"
            }
        return Response(msg, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if 'user' in request.data:
            try:
                user = User.objects.get(pk = request.data['user'])
            except User.DoesNotExist as erro:
                return Response({"user": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

            if user != request.user:
                return Response({'user': "Usuário Inválido."}, status=status.HTTP_403_FORBIDDEN)

        return super(LancamentosCaixaViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):        
        return super(LancamentosCaixaViewSet, self).partial_update(request, *args, **kwargs)
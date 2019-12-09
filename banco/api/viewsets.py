from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from banco.models import ContaBanco, LancamentosBanco
from caixa.models import Categoria
from usuario.models import UsuarioProfile
from django.contrib.auth.models import User
from .serializers import ContaBancoSerializer, LancamentosBancoSerializer
from rest_framework import status
from django.db.models import ProtectedError

class ContaBancoViewSet(ModelViewSet):
    serializer_class = ContaBancoSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        return ContaBanco.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):        
        return super(ContaBancoViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if 'user' not in request.data:
            return Response({"user": "O usuário é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        if request.data['tipo'] != ContaBanco.CONTA_BANCARIA:
            return Response({"tipo": "O tipo para agência bancária deve ser igual a 1."}, status=status.HTTP_400_BAD_REQUEST)

        if 'user' in request.data:
            try:
                user = User.objects.get(pk = request.data['user'])
            except User.DoesNotExist as erro:
                return Response({"user": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

            if user != request.user:
                return Response({'user': "Não é possível criar agência para outro usuário."}, status=status.HTTP_403_FORBIDDEN)
        
        return super(ContaBancoViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError as identifier:
            msg = "Não é possível excluir uma agência que possua lançamentos!"
            return Response({'erro': msg}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        msg = {
            "message: A agência " + instance.banco + " foi excluída com sucesso"
            }
        return Response(msg, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if 'user' in request.data:
            try:
                user = User.objects.get(pk = request.data['user'])
            except User.DoesNotExist as erro:
                return Response({"user": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

            if user != request.user:
                return Response({'user': "Usuário inválido."}, status=status.HTTP_403_FORBIDDEN)

        return super(ContaBancoViewSet, self).update(request, *args, **kwargs)


class LancamentosBancoViewSet(ModelViewSet):
    serializer_class = LancamentosBancoSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        return LancamentosBanco.objects.filter(user=self.request.user)

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

        if 'banco' in request.data:
           if not ContaBanco.bancoIsValid(user, request.data['banco']):
                return Response({"banco": "Banco não encontrado."}, status=status.HTTP_404_NOT_FOUND)
       
        return super(LancamentosBancoViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError as identifier:
            msg = "Não é possível excluir um lançamento que possua conta a pagar/receber!"
            return Response({'erro': msg}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        msg = {
            "message: O lançamento " + instance.descricao + " foi excluída com sucesso"
            }
        return Response(msg, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user = request.user

        if 'user' in request.data:
            try:
                user_request = User.objects.get(pk = request.data['user'])
            except User.DoesNotExist as erro:
                return Response({"user": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

            if user_request != user:
                return Response({'user': "Usuário inválido."}, status=status.HTTP_403_FORBIDDEN)

        if 'banco' in request.data:
           if not ContaBanco.bancoIsValid(user, request.data['banco']):
                return Response({"banco": "Banco não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        return super(LancamentosBancoViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not 'user' in request.data:
            return Response({"user": "Usuário é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        if 'banco' in request.data:
           if not ContaBanco.bancoIsValid(request.user, request.data['banco']):
                return Response({"banco": "Banco não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        return super(LancamentosBancoViewSet, self).partial_update(request, *args, **kwargs)

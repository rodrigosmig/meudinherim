from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from banco.models import ContaBanco
from usuario.models import UsuarioProfile
from django.contrib.auth.models import User
from .serializers import ContaBancoSerializer
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
                return Response({'user': "Não é possível atribuir categorias para outro usuário."}, status=status.HTTP_403_FORBIDDEN)

        return super(ContaBancoViewSet, self).update(request, *args, **kwargs)
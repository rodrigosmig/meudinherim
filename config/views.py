from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from usuario.forms import EditAccountsForm, UsuarioProfileForm
from usuario.models import UsuarioProfile
from banco.models import ContaBanco, LancamentosBanco, SaldoBanco
from caixa.models import Categoria, SaldoCaixa
from banco.forms import ContaBancoForm, LancamentosBancoForm
from caixa.forms import LancamentosForm
from django import forms
from caixa.views import separarCategorias
from django.contrib import messages


@login_required
def config(request):
    id_user = request.user.id
    template = 'config/config.html'
    contexto = {}

    user = User.objects.get(pk = id_user)
    formSenha = PasswordChangeForm(user = request.user)
    formDados = EditAccountsForm(instance = request.user)

    formUser = UsuarioProfileForm()
    contexto['formUser'] = formUser
    #Editar
    if(request.method == 'POST'):
        if(request.POST.get('old_password')):
            formSenha = PasswordChangeForm(data = request.POST, user = request.user)
            if formSenha.is_valid():
                formSenha.save()
                formSenha = PasswordChangeForm(user = request.user)
                messages.success(request, "Senha alterada com sucesso!")
        elif(request.FILES):
            userProfile = UsuarioProfile.objects.get(user = request.user)
            form = UsuarioProfileForm(request.POST, request.FILES, instance = userProfile)
            if(form.is_valid()):
                form.save()
                messages.success(request, "Imagem alterada com sucesso!")
        elif(request.POST.get('mail_contas_a_pagar')):
            lista = request.POST.getlist('mail_contas_a_pagar')
            userProfile = UsuarioProfile.objects.get(user = request.user)
            if(not userProfile.mail_contas_a_pagar and (lista[0] == 'on')):
                userProfile.mail_contas_a_pagar = True
                userProfile.save()
            elif(userProfile.mail_contas_a_pagar and (lista[0] == '0')):
                userProfile.mail_contas_a_pagar = False
                userProfile.save()
            messages.success(request, "Alerta alterado com sucesso!")
        else:
            #form = UsuarioProfileForm(request.POST, request.FILES)
            formDados = EditAccountsForm(request.POST, instance = request.user)
            if formDados.is_valid():
                formDados.save()
                formDados = EditAccountsForm(instance = request.user)
                formDados.fields['username'].widget.attrs.update({'readonly': 'readonly'}) #não permite que o usuário altere o username
                messages.success(request, "Usuário alterado com sucesso!")
        
    formSenha.fields['old_password'] = forms.CharField(
        label = 'Senha atual',
        max_length = 32,
        required = True,
        widget = forms.PasswordInput(
            attrs = {'class': 'form-control', 'placeholder': 'Senha atual', }
        )
    )

    formSenha.fields['new_password1'] = forms.CharField(
        label = 'Nova senha',
        max_length = 32,
        required = True,
        widget = forms.PasswordInput(
            attrs = {'class': 'form-control', 'placeholder': 'Nova senha', }
        )
    )

    formSenha.fields['new_password2'] = forms.CharField(
        label = 'Confirmaçao da nova senha',
        max_length = 32,
        required = True,
        widget = forms.PasswordInput(
            attrs = {'class': 'form-control', 'placeholder': 'Confirme a senha', }
        )
    )

    #para adicionar lancamento
    formCaixa = LancamentosForm()
    formCaixa.getAddLancamentoForm(request)
    contexto['formLancCaixa'] = formCaixa

    formBanco = LancamentosBancoForm()
    formBanco.getAddLancamentoForm(request, 'banco')
    contexto['formLancBanco'] = formBanco

    formCredito = LancamentosBancoForm()
    formCredito.getAddLancamentoForm(request, 'credito')
    contexto['formLancCredito'] = formCredito

    userProfile = UsuarioProfile.objects.get(user = request.user)
    contexto['profile'] = userProfile

    #busca o saldo de Caixa do usuario e atribui ao contexto
    saldoC = SaldoCaixa.objects.get(user = request.user)
    contexto['saldoCaixa'] = saldoC.saldoAtual

    #para saldo de cada agencia
    agencias = ContaBanco.objects.filter(user = request.user)
    contexto['agencias'] = agencias

    contexto['isPerfil'] = True

    contexto['userProfile'] = userProfile
    
    return render(request, template, contexto)

@login_required
def editoFoto(request):
    if(request.method == 'POST'):
        foto = UsuarioProfile.objects.get(user = request.user)
        form = UsuarioProfileForm(request.POST, request.FILES, instance = foto)
        if(form.is_valid()):
            form.save()
            return HttpResponseRedirect('/config/')

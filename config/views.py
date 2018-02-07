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


@login_required
def config(request):
    id_user = request.user.id
    template = 'config/config.html'
    contexto = {}

    user = User.objects.get(pk = id_user)
    formSenha = PasswordChangeForm(user = request.user)

    formFoto = UsuarioProfileForm()
    contexto['formFoto'] = formFoto

    #Editar
    if(request.method == 'POST'):
        form = UsuarioProfileForm(request.POST, request.FILES)
        print(form)
        formDados = EditAccountsForm(request.POST, instance = request.user)
        if formDados.is_valid():
            formDados.save()
            formDados = EditAccountsForm(instance = request.user)
            contexto['success'] = True
    else:
        formDados = EditAccountsForm(instance = request.user)

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

    formCaixa = LancamentosForm()
    #Seleciona apenas o banco do usuario para o formulario
    formCaixa.fields['categoria'].choices = separarCategorias(request)
    
    formBanco = LancamentosBancoForm()
    #Seleciona apenas o banco do usuario para o formulario
    formBanco.fields['banco'] = forms.ModelChoiceField(
        queryset = ContaBanco.objects.filter(user_id = request.user.id),
        empty_label = 'Nenhum',
        widget = forms.Select(
            attrs = {'class': 'form-control'}
        )
    )
    #seleciona apenas as categorias do usuario logado
    formBanco.fields['categoria'].choices = separarCategorias(request)

    #para adicionar lancamento
    contexto['formLancCaixa'] = formCaixa
    contexto['formLancBanco'] = formBanco

    contexto['formConfig'] = formDados
    contexto['formSenha'] = formSenha

    userProfile = UsuarioProfile.objects.get(user = request.user)
    contexto['profile'] = userProfile

    #busca o saldo de Caixa do usuario e atribui ao contexto
    saldoC = SaldoCaixa.objects.get(user = request.user)
    contexto['saldoCaixa'] = saldoC.saldoAtual

    #para saldo de cada agencia
    agencias = ContaBanco.objects.filter(user = user)
    contexto['agencias'] = agencias
    
    return render(request, template, contexto)

@login_required
def editSenha(request):
    template = 'config/config.html'
    contexto = {}
    formDados = EditAccountsForm(instance = request.user)

    #Editar Senha
    if(request.method == 'POST'):
        formSenha = PasswordChangeForm(data = request.POST, user = request.user)
        if formSenha.is_valid():
            formSenha.save()
            contexto['success'] = True
        else:
            contexto['erros'] = True
            contexto['mensagem'] = 'Senha não alterada. Tente novamente'
            
    else:
        formSenha = PasswordChangeForm(user = request.user)

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

    contexto['formSenha'] = formSenha
    contexto['formConfig'] = formDados

    formCaixa = LancamentosForm()
    #Seleciona apenas o banco do usuario para o formulario
    formCaixa.fields['categoria'].choices = separarCategorias(request)
    
    formBanco = LancamentosBancoForm()
    #Seleciona apenas o banco do usuario para o formulario
    formBanco.fields['banco'] = forms.ModelChoiceField(
        queryset = ContaBanco.objects.filter(user_id = request.user.id),
        empty_label = 'Nenhum',
        widget = forms.Select(
            attrs = {'class': 'form-control'}
        )
    )
    #seleciona apenas as categorias do usuario logado
    formBanco.fields['categoria'].choices = separarCategorias(request)

    return render(request, template, contexto)

@login_required
def editoFoto(request):
    if(request.method == 'POST'):
        foto = UsuarioProfile.objects.get(user = request.user)
        form = UsuarioProfileForm(request.POST, request.FILES, instance = foto)
        if(form.is_valid()):
            form.save()
            return HttpResponseRedirect('/config/')

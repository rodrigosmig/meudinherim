from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from banco.models import ContaBanco, LancamentosBanco, SaldoBanco
from caixa.models import Categoria, SaldoCaixa
from banco.forms import ContaBancoForm, LancamentosBancoForm
from caixa.forms import LancamentosForm
from django import forms
from usuario.models import UsuarioProfile
from django.core import serializers
import json

@login_required
def cadastroBanco(request):

	if (request.method == 'POST'):
		form = ContaBancoForm(request.POST)
		if (form.is_valid):
			bancos = form.save(commit = False)
			bancos.user = request.user 
			bancos.save()
			return HttpResponse('Agência cadastrada com sucesso.')
		else:
			return HttpResponseServerError('Formulário inválido.')

	user = request.user

	template = 'banco/agencia.html'
	agencias = ContaBanco.objects.filter(user = user)
	form_agencia = ContaBancoForm()

	contexto = {'formAgencia': form_agencia, 'agencias': agencias}

	#busca o saldo de Caixa do usuario e atribui ao contexto
	saldoC = SaldoCaixa.objects.get(user = user)
	contexto['saldoCaixa'] = saldoC.saldoAtual

	userProfile = UsuarioProfile.objects.get(user = user)
	contexto['profile'] = userProfile

	#para adicionar lancamento
	formCaixa = LancamentosForm()
	#seleciona apenas as categorias do usuario logado
	formCaixa.fields['categoria'] = forms.ModelChoiceField(
			queryset = Categoria.objects.filter(user = user),
			empty_label = 'Nenhum',
	        widget = forms.Select(
	            attrs = {'class': 'form-control'}
	        )
		)
	#para adicionar lancamento
	formBanco = LancamentosBancoForm()
	#Seleciona apenas o banco do usuario para o formulario
	formBanco.fields['banco'] = forms.ModelChoiceField(
		queryset = ContaBanco.objects.filter(user = user),
		empty_label = 'Nenhum',
        widget = forms.Select(
            attrs = {'class': 'form-control'}
        )
	)
	#seleciona apenas as categorias do usuario logado
	formBanco.fields['categoria'] = forms.ModelChoiceField(
			queryset = Categoria.objects.filter(user = user),
			empty_label = 'Nenhum',
	        widget = forms.Select(
	            attrs = {'class': 'form-control', 'id': 'categoria_banco'}
	        )
		)
	#para adicionar lancamento
	contexto['formLancCaixa'] = formCaixa
	contexto['formLancBanco'] = formBanco
	

	return render(request, template, contexto)

@login_required
def banco(request):
	#usuario logado
	user = request.user

	if(request.method == 'POST'):

		agencia = request.POST.get('agencia')
		mes = request.POST.get('mes')
		ano = request.POST.get('ano')

		agencia = ContaBanco.objects.get(pk = agencia)

		lancamentos = LancamentosBanco.objects.filter(data__month = mes).filter(data__year = ano).filter(user = user).filter(banco = agencia)

		if(len(lancamentos) != 0):
			lancJson = serializers.serialize('json', lancamentos, use_natural_foreign_keys=True, use_natural_primary_keys=True)
			
			return HttpResponse(lancJson, content_type="application/json")
		else:
			return HttpResponseServerError("Nenhum lançamento foi encontrado.")

	template = 'banco/banco.html'
	contexto = {}

	listAgencias = []
	todasAgencias = ContaBanco.objects.filter(user = user)

	for a in todasAgencias:
		id = a.id
		nome = a.banco
		saldo = str(a.saldo)
		listAgencias.append((id, nome, saldo))


	listAgencias = [{'id': id, 'agencia': agencia, 'saldo': saldo} for id, agencia, saldo in listAgencias]
	listAgencias = json.dumps(listAgencias, ensure_ascii=False)
	contexto['selectAgencias'] = listAgencias

	formCaixa = LancamentosForm()
	#seleciona apenas as categorias do usuario logado
	formCaixa.fields['categoria'] = forms.ModelChoiceField(
			queryset = Categoria.objects.filter(user = user),
			empty_label = 'Nenhum',
	        widget = forms.Select(
	            attrs = {'class': 'form-control'}
	        )
		)
	
	formBanco = LancamentosBancoForm()
	#Seleciona apenas o banco do usuario para o formulario
	formBanco.fields['banco'] = forms.ModelChoiceField(
		queryset = ContaBanco.objects.filter(user = user),
		empty_label = 'Nenhum',
        widget = forms.Select(
            attrs = {'class': 'form-control'}
        )
	)
	#seleciona apenas as categorias do usuario logado
	formBanco.fields['categoria'] = forms.ModelChoiceField(
			queryset = Categoria.objects.filter(user = user),
			empty_label = 'Nenhum',
	        widget = forms.Select(
	            attrs = {'class': 'form-control', 'id': 'categoria_banco'}
	        )
		)

	#para adicionar lancamento
	contexto['formLancCaixa'] = formCaixa
	contexto['formLancBanco'] = formBanco

	userProfile = UsuarioProfile.objects.get(user = user)
	contexto['profile'] = userProfile	

	#para saldo da carteira
	saldoC = SaldoCaixa.objects.get(user = user)
	contexto['saldoCaixa'] = saldoC.saldoAtual

	#para saldo de cada agencia
	agencias = ContaBanco.objects.filter(user = user)
	contexto['agencias'] = agencias	

	return render(request, template, contexto)

@login_required
def addLancamento(request):
	if(request.method == 'POST'):
		
		form = LancamentosBancoForm(request.POST)
		agencia = request.POST.get('banco')
		
		if(form.is_valid()):
			lancamento = form.save(commit = False)

			conta = ContaBanco.objects.get(pk = agencia)

			if (lancamento.tipo == "1"):				
				conta.saldo += lancamento.valor
			else:
				conta.saldo -= lancamento.valor

			conta.save()

			#relacionao o usuario logado com o lançamento
			lancamento.user = request.user
			lancamento.save()
			return HttpResponse('Lançamento efetuado com sucesso.')
	return HttpResponseServerError('Lançamento inválido')

@login_required
def editLancamento(request):

	if(request.method == 'POST'):

		id_user = request.user.id

		agencia = request.POST.get('banco')

		#id do lancamento clicado
		idLancamento = request.POST.get('id')
		#busca o lancamento a ser alterado
		lancamento = LancamentosBanco.objects.get(pk = idLancamento)
		#atribui o lancamento ao form	
		form = LancamentosBancoForm(request.POST, instance = lancamento)

		if(form.is_valid()):			
			form.save()
			conta = ContaBanco.objects.get(pk = agencia)
			lancamentos = LancamentosBanco.objects.filter(user_id = id_user).filter(banco = agencia)
			saldo = 0

			for l in lancamentos:
				if (l.tipo == '1'):
					saldo += l.valor
				else:
					saldo -= l.valor			
			conta.saldo = saldo 

			conta.save()			

			return HttpResponse("Lançamento alterado com sucesso")
		else:
			return HttpResponseServerError("Formulário inválido")

	#id do lancamento clicado
	idLancamento = request.GET.get('id')
	lancamento = LancamentosBanco.objects.get(pk = idLancamento)	
	form = LancamentosBancoForm(instance = lancamento)

	#seleciona apenas os banco do usuario logado
	form.fields['banco'] = forms.ModelChoiceField(
			queryset = ContaBanco.objects.filter(user_id = request.user.id),
			empty_label = 'Nenhum',
	        widget = forms.Select(
	            attrs = {'class': 'form-control', 'id': 'id_banco-alter_banco'}
	        )
		)
	#seleciona apenas as categorias do usuario logado
	form.fields['categoria'] = forms.ModelChoiceField(
			queryset = Categoria.objects.filter(user_id = request.user.id),
			empty_label = 'Nenhum',
	        widget = forms.Select(
	            attrs = {'class': 'form-control', 'id': 'id_categoria-alter_banco'}
	        )
		)
	form.fields['data'] = forms.DateField(
		label = 'Data',
		required = True,
		widget = forms.TextInput(
			attrs = {'class': 'form-control', 'id': 'datepicker-alter_banco'}
		)
    )
	form.fields['tipo'] = forms.ChoiceField(
		widget = forms.Select(
            attrs = {'class': 'form-control', 'id': 'id_tipo-alter_banco'}
        ),
        choices = LancamentosBanco.TIPOS
    )
	form.fields['valor'] = forms.DecimalField(
		label = 'Valor',
        min_value = 0.01,
        max_value = 9999.99,
        required = True,
        widget = forms.NumberInput(
            attrs = {'class': 'form-control', 'id': 'id_valor-alter_banco'}
        )
    )
	form.fields['descricao'] = forms.CharField(
		label = 'Descrição',
		max_length = 32,
		required = True,
		widget = forms.TextInput(
		attrs = {'class': 'form-control', 'id': 'id_descricao-alter_banco'}
        )
    )

	if(lancamento.conta_a_pagar != None):
		contaID = "<div id='status_conta'>Pago</div>"
	elif(lancamento.conta_a_receber != None):
		contaID = "<div id='status_conta'>Recebido</div>"
	else:
		contaID = "<div id='status_conta'>Nenhum</div>"

	#retorna o id do lancamento junto com o formulario
	divId = "<div id='id_lancamento'>" + idLancamento + "</div>"

	form_html = {form.as_p(), divId, contaID}
	return HttpResponse(form_html)

@login_required
def delLancamento(request):

	if(request.method == 'POST'):
		
		id_user = request.user.id

		#id do lancamento a ser deletado
		idLancamento = request.POST.get('id')

		#busca o lançamento
		lancamento = LancamentosBanco.objects.get(pk = idLancamento)

		if(request.user.id == lancamento.user_id):
			lancamento.delete()

			agencia = request.POST.get('banco')
			conta = ContaBanco.objects.get(pk = agencia)
			lancamentos = LancamentosBanco.objects.filter(user_id = id_user).filter(banco = agencia)
			saldo = 0

			for l in lancamentos:
				
				if (l.tipo == '1'):
					saldo += l.valor
				else:
					saldo -= l.valor			
			conta.saldo = saldo 

			conta.save()

			return HttpResponse("Lançamento excluído com sucesso.")
		else:
			return HttpResponseServerError("Lançamento não encontrado.")
		

	return HttpResponseServerError("Lançamento não encontrado.")

@login_required
def editAgencia(request):

	if (request.method == 'POST'):

		id_usuario = request.user.id 

		# id da agencia clicada
		idAgencia = request.POST.get('id')
	
		agencia = ContaBanco.objects.get(pk = idAgencia)

		form = ContaBancoForm(request.POST,instance = agencia)

		if (form.is_valid()):
			form.save()

			return HttpResponse("Agência alterada com sucesso.")

		else:

			return HttpResponseServerError("Formulário inválido")

	# id da agencia clicada
	idAgencia = request.GET.get('idAgencia')

	agencia = ContaBanco.objects.get(pk = idAgencia)
	
	form = ContaBancoForm(instance = agencia)

	# redefine id do campo banco
	form.fields['banco'] = forms.CharField(
			#queryset = ContaBanco.objects.filter(user_id = request.user.id),
			label = 'Banco',
			max_length = 32,
			required = True,
	        widget = forms.TextInput(
	            attrs = {'class': 'form-control', 'id':'id_banco-alter_banco', 'placeholder': 'Nome do Banco'}
	        )
	)

	form.fields['agencia'] = forms.CharField(
			label = 'Agência',
			max_length = 12,
			required = False,
	        widget = forms.TextInput(
	            attrs = {'class': 'form-control', 'id':'id_agencia-alter_agencia', 'placeholder': 'Nome da Agência'}
	        )
	)

	form.fields['conta'] = forms.CharField(
			label = 'Conta',
			max_length = 32,
			required = False,
	        widget = forms.TextInput(
	            attrs = {'class': 'form-control', 'id':'id_conta-alter_conta', 'placeholder': 'Número da Conta'}
	        )
	)

	form.fields['tipo'] = forms.ChoiceField(

		widget = forms.Select(
			attrs = {'class': 'form-control', 'id':'id_tipo-alter_tipo'}
		),
		choices = ContaBanco.TIPOS
	)
	temp = 'id_agencia-alter_agencia'
	#retorna o id do agencia junto com o formulario
	divId = "<div id=temp>" + idAgencia + "</div>"
	form_html = {form.as_p(), divId}
	return HttpResponse(form_html)

@login_required
def delAgencia(request):

	if (request.method == 'POST'):
		
		id_usuario = request.user.id 

		idAgencia =  request.POST.get('id')

		agencia = ContaBanco.objects.get(pk = idAgencia)

		if(id_usuario == agencia.user.id):
			agencia.delete()
			return HttpResponse("Agência excluída com sucesso.")
		else:
			return HttpResponseServerError("Agência não econtrada")
	return HttpResponseServerError("Agência não econtrada")

@login_required
def verificarContas(request):
	if(request.method == 'POST'):
		idLancamentoBanco = request.POST.get('id')
		lancamento = LancamentosBanco.objects.get(pk = idLancamentoBanco)
		if(lancamento.conta_a_pagar != None):
			return HttpResponseServerError('Lançamento realizado pelo contas a pagar. Para excluir este lançamento, cancele seu pagamento em Contas a Pagar.')
		elif(lancamento.conta_a_receber != None):
			return HttpResponseServerError('Lançamento realizado pelo contas a receber. Para excluir este lançamento, cancele seu recebimento em Contas a Receber.')
		else:
			return HttpResponse(idLancamentoBanco)

	else:
		HttpResponseServerError("Conta inexistente")
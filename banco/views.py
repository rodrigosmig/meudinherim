from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from banco.models import ContaBanco, LancamentosBanco, SaldoBanco
from caixa.models import Categoria, SaldoCaixa
from banco.forms import ContaBancoForm, LancamentosBancoForm
from caixa.forms import LancamentosForm
from django import forms

@login_required
def cadastroBanco(request):

	if (request.method == 'POST'):
		form = ContaBancoForm(request.POST)
		if (form.is_valid):
			bancos = form.save(commit = False)
			bancos.user = request.user 
			bancos.save()
			return HttpResponseRedirect('/banco/agencia')

	id_user = request.user.id

	template = 'banco/agencia.html'
	agencias = ContaBanco.objects.filter(user_id = id_user)
	form_agencia = ContaBancoForm()

	contexto = {'formAgencia': form_agencia, 'agencias': agencias}

	#busca o saldo de Caixa do usuario e atribui ao contexto
	saldoC = SaldoCaixa.objects.get(user = request.user)
	contexto['saldoCaixa'] = saldoC.saldoAtual

	#busca o saldo de Banco do usuario e atribui ao contexto
	saldoB = SaldoBanco.objects.get(user = request.user)
	contexto['saldoBanco'] = saldoB.saldoAtual

	return render(request, template, contexto)

@login_required
def banco(request):
	#id do usuario logado
	id_user = request.user.id
	template = 'banco/banco.html'
	lancamentos = LancamentosBanco.objects.filter(user_id = id_user)

	saldoB = SaldoBanco.objects.get(user = request.user)
	saldoC = SaldoCaixa.objects.get(user = request.user)


	contexto = {'lancBanco': lancamentos,'saldoBanco' : saldoB.saldoAtual,
	 'saldoCaixa': saldoC.saldoAtual}

	formCaixa = LancamentosForm()
	#seleciona apenas as categorias do usuario logado
	formCaixa.fields['categoria'] = forms.ModelChoiceField(
			queryset = Categoria.objects.filter(user_id = request.user.id),
			empty_label = 'Nenhum',
	        widget = forms.Select(
	            attrs = {'class': 'form-control'}
	        )
		)
	
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
	formBanco.fields['categoria'] = forms.ModelChoiceField(
			queryset = Categoria.objects.filter(user_id = request.user.id),
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
def addLancamento(request):
	if(request.method == 'POST'):
		
		form = LancamentosBancoForm(request.POST)
		
		if(form.is_valid()):
			lancamento = form.save(commit = False)

			saldo = SaldoBanco.objects.get(user = request.user)

			saldo.saldoAnterior = saldo.saldoAtual

			if (lancamento.tipo == "1"):
				
				saldo.saldoAtual += lancamento.valor
			else:
				saldo.saldoAtual -= lancamento.valor

			saldo.save()

			#relacionao o usuario logado com o lançamento
			lancamento.user = request.user
			lancamento.save()
			return HttpResponse('Lançamento efetuado com sucesso.')
	return HttpResponseServerError('Lançamento inválido')

@login_required
def editLancamento(request):

	if(request.method == 'POST'):

		id_user = request.user.id

		#id do lancamento clicado
		idLancamento = request.POST.get('id')
		#busca o lancamento a ser alterado
		lancamento = LancamentosBanco.objects.get(pk = idLancamento)
		#atribui o lancamento ao form	
		form = LancamentosBancoForm(request.POST, instance = lancamento)

		if(form.is_valid()):
			form.save()

			saldoBanco = SaldoBanco.objects.get(user = request.user)
			lancamentos = LancamentosBanco.objects.filter(user_id = id_user)

			saldo = 0
			for l in lancamentos:
				if (l.tipo == '1'):
					saldo += l.valor
				else:
					saldo -= l.valor
			
			saldoBanco.saldoAtual = saldo 
			saldoBanco.save()

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
	            attrs = {'class': 'form-control'}
	        )
		)
	#seleciona apenas as categorias do usuario logado
	form.fields['categoria'] = forms.ModelChoiceField(
			queryset = Categoria.objects.filter(user_id = request.user.id),
			empty_label = 'Nenhum',
	        widget = forms.Select(
	            attrs = {'class': 'form-control', 'id': 'categoria_banco'}
	        )
		)

	#retorna o id do lancamento junto com o formulario
	divId = "<div id='id_lancamento'>" + idLancamento + "</div>"

	form_html = {form.as_p(), divId}
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


			saldoBanco = SaldoBanco.objects.get(user=request.user)
			lancamentos = LancamentosBanco.objects.filter(user_id=id_user)

			saldo = 0
			for l in lancamentos:
				if(l.tipo == '1'):
					saldo += l.valor
				else:
					saldo -= l.valor

			saldoBanco.saldoAtual = saldo 
			saldoBanco.save()

			return HttpResponse("Lançamento excluído com sucesso")
		else:
			return HttpResponseServerError("Lançamento não encontrado.")
		

	return HttpResponseServerError("Lançamento não encontrado.")

def editAgencia(request):

	if (request.method == 'POST'):

		id_usuario = request.user.id 

		# id da agencia clicada
		idAgencia = request.POST.get('id')
	
		agencia = ContaBanco.objects.get(pk = idAgencia)

		form = ContaBancoForm(request.POST,instance = agencia)

		print (idAgencia+" dentro do post")
		if (form.is_valid()):
			form.save()

			return HttpResponse("Agência alterada com sucesso")

		else:

			return HttpResponseServerError("Formulário inválido")

	# id da agencia clicada
	idAgencia = request.GET.get('idAgencia')

	print (idAgencia+" depois do post")

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


def delAgencia(request):

	if (request.method == 'POST'):
		
		id_usuario = request.user.id 

		idAgencia =  request.POST.get('id')

		agencia = ContaBanco.objects.get(pk = idAgencia)

		if(id_usuario == agencia.user.id):
			agencia.delete()
			return HttpResponse("Agência excluída")
		else:
			return HttpResponseServerError("não econtrado")
	return HttpResponseServerError("não econtrado")
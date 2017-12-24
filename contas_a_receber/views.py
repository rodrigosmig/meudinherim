from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from caixa.models import Categoria, SaldoCaixa, LancamentosCaixa
from banco.models import SaldoBanco, ContaBanco, LancamentosBanco
from banco.forms import LancamentosBancoForm
from caixa.forms import LancamentosForm
from contas_a_receber.models import ContasAReceber
from contas_a_receber.forms import ContasAReceberForm
from django import forms

@login_required
def contasAReceber(request):
	user = request.user

	if(request.method == 'POST'):
		form = ContasAReceberForm(request.POST)

		if(form.is_valid()):
			contReceber = form.save(commit = False)
			contReceber.user = user
			contReceber.recebido = False
			contReceber.save()

			return HttpResponse("Conta a receber adicionada com sucesso.")
		else:
			return HttpResponseServerError("Formulário inválido.")


	template = 'contas_a_receber/contas_a_receber.html'

	contas = ContasAReceber.objects.filter(user = user)

	form = ContasAReceberForm()

	form.fields['categoria'] = forms.ModelChoiceField(
        queryset = Categoria.objects.filter(user = user).filter(tipo = 1),
        empty_label = 'Nenhum',
        widget = forms.Select(
            attrs = {'class': 'form-control'}
        )
    )

	contexto = {'contReceber': contas, 'contReceberForm': form}

	#busca o saldo de Caixa do usuario e atribui ao contexto
	saldoC = SaldoCaixa.objects.get(user = request.user)
	contexto['saldoCaixa'] = saldoC.saldoAtual

	#busca o saldo de Banco do usuario e atribui ao contexto
	saldoB = SaldoBanco.objects.get(user = request.user)
	contexto['saldoBanco'] = saldoB.saldoAtual

	return render(request, template, contexto)

@login_required
def editContasReceber(request):
	user = request.user

	if(request.method == 'POST'):

		#id da conta clicado
		idConta = request.POST.get('id')
		print(idConta, 'teste')
		#busca o lancamento a ser alterado
		conta = ContasAReceber.objects.get(pk = idConta)
		
		#atribui o lancamento ao form	
		form = ContasAReceberForm(request.POST, instance = conta)
		
		if(form.is_valid()):
			form.save()

			return HttpResponse("Conta alterada com sucesso")
		else:
			return HttpResponseServerError("Formulário inválido.")

	#id do lancamento clicado
	idConta = request.GET.get('id')
	print(id)
	conta = ContasAReceber.objects.get(pk = idConta)
	form = ContasAReceberForm(instance = conta)

	#seleciona apenas as categorias do usuario logado e do tipo entrada
	form.fields['categoria'] = forms.ModelChoiceField(
			queryset = Categoria.objects.filter(user = user).filter(tipo = 1),
			empty_label = 'Nenhum',
	        widget = forms.Select(
	            attrs = {'class': 'form-control', 'id': 'id_categoria_edit'}
	        )
		)

	#altera o id dos campos
	form.fields['data'] = forms.DateField(
		label = 'Data',
		required = True,
		widget = forms.TextInput(
			attrs = {'class': 'form-control', 'id': 'datepickerCR_edit'}

        )
	)
	form.fields['descricao'] = forms.CharField(
		label = 'Descrição',
		max_length = 32,
		required = True,
		widget = forms.TextInput(
			attrs = {'class': 'form-control', 'id': 'id_descricao_edit'}
        )
    )
	form.fields['valor'] = forms.DecimalField(
		label = 'Valor',
		min_value = 0.01,
    	max_value = 999999.99,
    	required = True,
    	widget = forms.NumberInput(
    		attrs = {'class': 'form-control', 'id': 'id_valor_edit'}
        )
    )

	#retorna o id da conta junto com o formulario
	divId = "<div id='id_contaAReceber'>" + idConta + "</div>"

	form_html = {form.as_p(), divId}

	return HttpResponse(form_html)

@login_required
def delContasReceber(request):
	if(request.method == 'POST'):
		#usuario
		user = request.user

		#id da conta a ser deletada
		idConta = request.POST.get('id')

		#busca a conta
		conta = ContasAReceber.objects.get(pk = idConta)		
		
		if(user == conta.user):
			conta.delete()
			
			return HttpResponse("Conta a receber excluída com sucesso")
		else:
			return HttpResponseServerError("Conta não encontrado.")
		

	return HttpResponseServerError("Conta não encontrado.")

@login_required
def recebimento(request):
	if(request.method == 'POST'):
		#usuario
		user = request.user

		tipoRecebimento = request.POST.get('banco')

		#busca o saldo do caixa do usuario logado
		saldoCaixa = SaldoCaixa.objects.get(user = request.user)
		#atribui o valor do saldo anterior
		saldoCaixa.saldoAnterior = saldoCaixa.saldoAtual

		#busca o saldo de Banco do usuario logado
		saldoBanco = SaldoBanco.objects.get(user = request.user)
		#atribui o valor do saldo anterior
		saldoBanco.saldoAnterior = saldoBanco.saldoAtual
		
		idConta = request.POST.get('id')

		#busca a conta a pagar
		conta = ContasAReceber.objects.get(pk = idConta)

		print(tipoRecebimento)
		#verifica se o pagamento é no caixa ou no banco
		if(tipoRecebimento == ""):
			#para pagamento feito no caixa
			conta.tipo_conta = "c"
			print('caixa')
			#cadastra o lancamento do caixa de acordo com os dados da conta
			caixa = LancamentosCaixa()

			caixa.data = conta.data
			caixa.categoria = conta.categoria
			caixa.descricao = conta.descricao
			caixa. valor = conta.valor
			caixa.user = request.user
			caixa.conta_a_receber = conta

			#diminui o saldo do usuário
			saldoCaixa.saldoAtual += caixa.valor
			
			caixa.save()
			saldoCaixa.save()
	
		else:
			#para pagamento feito no banco
			conta.tipo_conta = "b"
			print('banco')
			agencias = ContaBanco.objects.filter(user = user)

			for agencia in agencias:
				if(agencia.banco == tipoRecebimento):
					banco = LancamentosBanco()

					banco.banco = agencia
					banco.data = conta.data
					banco.tipo = '1'
					banco.categoria = conta.categoria
					banco.descricao = conta.descricao
					banco. valor = conta.valor
					banco.user = request.user
					banco.conta_a_receber = conta
					
					saldoBanco.saldoAtual += banco.valor

					banco.save()
					saldoBanco.save()

		conta.recebido = True
		conta.save()
		
		return HttpResponse("Recebimento efetuado com sucesso.")

@login_required
def cancelaRecebimento(request):
	if(request.method == 'POST'):
		user = request.user
		idRecebimento = request.POST.get('id')

		conta = ContasAReceber.objects.get(pk = idRecebimento)

		if(conta.user == user):
			if(conta.tipo_conta == "c"):
				#busca o lançamento gerado pelo recebimento
				lancamentoCaixa = LancamentosCaixa.objects.get(conta_a_receber = conta)
				#deleta o lançamento gerado pelo recebimento
				lancamentoCaixa.delete()
				#muda o status do recebimento
				conta.recebido = False
				#deixa em branco o tipo da conta de recebimento
				conta.tipo_conta = None

				#busca o saldo do caixa do usuario logado e faz o ajuste
				saldoCaixa = SaldoCaixa.objects.get(user = user)
				saldoCaixa.saldoAnterior = saldoCaixa.saldoAtual
				saldoCaixa.saldoAtual -= conta.valor
				saldoCaixa.save()
				conta.save()
			
			else:
				#busca o lançamento gerado pelo recebimento
				lancamentoBanco = LancamentosBanco.objects.get(conta_a_receber = conta)
				#deleta o lançamento gerado pelo recebimento
				lancamentoBanco.delete()
				#muda o status do recebimento
				conta.recebido = False
				#deixa em branco o tipo da conta de recebimento
				conta.tipo_conta = None

				#busca o saldo do caixa do usuario logado e faz o ajuste
				saldoBanco = SaldoBanco.objects.get(user = user)
				saldoBanco.saldoAnterior = saldoBanco.saldoAtual
				saldoBanco.saldoAtual -= conta.valor
				saldoBanco.save()
				conta.save()

			return HttpResponse('Recebimento cancelado com sucesso.')


	return HttpResponseServerError("Pagamento não encontrado. Tente novamente.")


@login_required
def verificarRecebimento(request):
	if(request.method == 'POST'):
		idRecebimento = request.POST.get('id')
		conta = ContasAReceber.objects.get(pk = idRecebimento)
		if(conta.recebido):
			return HttpResponseServerError('Conta foi recebida. Cancele o recebimento antes de excluir.')
		else:
			return HttpResponse(idRecebimento)
	else:
		HttpResponseServerError("Conta inexistente")

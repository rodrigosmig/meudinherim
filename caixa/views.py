from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from caixa.models import LancamentosCaixa, Categoria, SaldoCaixa
from caixa.forms import CategoriaForm, LancamentosForm
from django.http import JsonResponse
from django import forms

@login_required
def lancamentos(request):
	#id do usuario logado
	saldo = 0
	id_user = request.user.id
	template = 'caixa/caixa.html'
	lancamentos = LancamentosCaixa.objects.filter(user_id = id_user)
	contexto = {'lancamentos': lancamentos}
  
	saldo = SaldoCaixa.objects.get(user = request.user)

	contexto['saldo'] = saldo.saldoAtual

	return render(request, template, contexto)

@login_required
def categoria(request):
	id_user = request.user.id
	template = 'caixa/categoria.html'
	catEntrada = Categoria.objects.filter(tipo = 1).filter(user_id = id_user)
	catSaida = Categoria.objects.filter(tipo = 2).filter(user_id = id_user)
	
	if(request.method == 'POST'):
		form = CategoriaForm(request.POST)
		if(form.is_valid()):
			categoria = form.save(commit = False)
			categoria.user = request.user
			categoria.save()
			return HttpResponseRedirect('/caixa/categoria')

	else:
		form = CategoriaForm()

	contexto = {'catEntrada': catEntrada, 'catSaida': catSaida, 'form': form}

	return render(request, template, contexto)


@login_required
def addLancamento(request):
	if(request.method == 'POST'):	
		form = LancamentosForm(request.POST)
		if(form.is_valid()):
			lancamento = form.save(commit = False)

			#busca o saldo do usuario logado
			saldo = SaldoCaixa.objects.get(user = request.user)
			#atribui o valor do saldo anterior
			saldo.saldoAnterior = saldo.saldoAtual

			#atribui o novo saldo de acordo com a categoria do lançamento
			if(lancamento.categoria.tipo == "1"):
				saldo.saldoAtual += lancamento.valor
			else:
				saldo.saldoAtual -= lancamento.valor
			
			#salva o novo saldo
			saldo.save()

			#relacionao o usuario logado com o lançamento
			lancamento.user = request.user
			lancamento.save()
			return HttpResponse('Lançamento efetuado com sucesso.')
	
	return ('Lançamento inválido')

@login_required
def editLancamento(request):

	if(request.method == 'POST'):
		#id do usuario
		id_user = request.user.id
		#id do lancamento clicado
		idLancamento = request.POST.get('id')
		#busca o lancamento a ser alterado
		lancamento = LancamentosCaixa.objects.get(pk = idLancamento)
		
		valorAtual = lancamento.valor
		categoriaAtual = lancamento.categoria.tipo

		#atribui o lancamento ao form	
		form = LancamentosForm(request.POST, instance = lancamento)

		
		if(form.is_valid()):
			form.save()

			#busca o saldo do usuario logado
			saldoCaixa = SaldoCaixa.objects.get(user = request.user)
			lancamentos = LancamentosCaixa.objects.filter(user_id = id_user)
			saldo = 0
			
			for l in lancamentos:
				if (l.categoria.tipo == '1'):
					saldo += l.valor
				else:
					saldo -= l.valor
								
			saldoCaixa.saldoAtual = saldo
			saldoCaixa.save()

			print(saldoCaixa.saldoAtual)

			return HttpResponse("Formulário alterado com sucesso")
		else:
			return HttpResponse("Formulário inválido")

	#id do lancamento clicado
	idLancamento = request.GET.get('id')
	lancamento = LancamentosCaixa.objects.get(pk = idLancamento)
	form = LancamentosForm(instance = lancamento)

	#seleciona apenas as categorias do usuario logado
	form.fields['categoria'] = forms.ModelChoiceField(
			queryset = Categoria.objects.filter(user_id = request.user.id),
			empty_label = 'Nenhum',
	        widget = forms.Select(
	            attrs = {'class': 'form-control'}
	        )
		)

	#retorna o id do lancamento junto com o formulario
	divId = "<div id='id_lancamento'>" + idLancamento + "</div>"

	form_html = {form.as_p(), divId}
	return HttpResponse(form_html)

@login_required
def delLancamento(request):
	if(request.method == 'POST'):
		#id do usuario
		id_user = request.user.id
		#id do lancamento a ser deletado
		idLancamento = request.POST.get('id')

		#busca o lançamento
		lancamento = LancamentosCaixa.objects.get(pk = idLancamento)		
		
		if(request.user.id == lancamento.user_id):
			lancamento.delete()
			#busca o saldo do usuario logado
			saldoCaixa = SaldoCaixa.objects.get(user = request.user)
			lancamentos = LancamentosCaixa.objects.filter(user_id = id_user)
			saldo = 0
			
			for l in lancamentos:
				if (l.categoria.tipo == '1'):
					saldo += l.valor
				else:
					saldo -= l.valor
								
			saldoCaixa.saldoAtual = saldo
			saldoCaixa.save()

			print(saldoCaixa.saldoAtual)

			return HttpResponse("Lançamento excluído com sucesso")
		else:
			return HttpResponse("Lançamento não encontrado.")
		

	return HttpResponse("Lançamento não encontrado.")

	
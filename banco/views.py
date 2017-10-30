from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError
from banco.models import ContaBanco, LancamentosBanco
from banco.forms import ContaBancoForm, LancamentosBancoForm
from django import forms

@login_required
def cadastroBanco(request):
	id_user = request.user.id

	template = 'banco/agencia.html'
	agencias = ContaBanco.objects.filter(user_id = id_user)
	form_agencia = ContaBancoForm()

	context = {'formAgencia': form_agencia, 'agencias': agencias}

	return render(request, template, context)

@login_required
def banco(request):
	#id do usuario logado
	id_user = request.user.id
	template = 'banco/banco.html'
	lancamentos = LancamentosBanco.objects.filter(user_id = id_user)
	contexto = {'lancBanco': lancamentos}

	return render(request, template, contexto)

@login_required
def addLancamento(request):
	if(request.method == 'POST'):
		print('entrou no if')
		form = LancamentosBancoForm(request.POST)
		if(form.is_valid()):
			lancamento = form.save(commit = False)
			#relacionao o usuario logado com o lançamento
			lancamento.user = request.user
			lancamento.save()
			return HttpResponse('Lançamento efetuado com sucesso.')
	return HttpResponseServerError('Lançamento inválido')

@login_required
def editLancamento(request):
	if(request.method == 'POST'):
		#id do lancamento clicado
		idLancamento = request.POST.get('id')
		#busca o lancamento a ser alterado
		lancamento = LancamentosBanco.objects.get(pk = idLancamento)
		#atribui o lancamento ao form	
		form = LancamentosBancoForm(request.POST, instance = lancamento)
		if(form.is_valid()):
			form.save()
			return HttpResponse("Lançamento alterado com sucesso")
		else:
			return HttpResponseServerError("Formulário inválido")

	#id do lancamento clicado
	idLancamento = request.GET.get('id')
	lancamento = LancamentosBanco.objects.get(pk = idLancamento)
	form = LancamentosBancoForm(instance = lancamento)

	form.fields['banco'] = forms.ModelChoiceField(
			queryset = ContaBanco.objects.filter(user_id = request.user.id),
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
		#id do lancamento a ser deletado
		idLancamento = request.POST.get('id')

		#busca o lançamento
		lancamento = LancamentosBanco.objects.get(pk = idLancamento)

		if(request.user.id == lancamento.user_id):
			lancamento.delete()
			return HttpResponse("Lançamento excluído com sucesso")
		else:
			return HttpResponseServerError("Lançamento não encontrado.")
		

	return HttpResponseServerError("Lançamento não encontrado.")
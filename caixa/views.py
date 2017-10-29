from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from caixa.models import LancamentosCaixa, Categoria
from caixa.forms import CategoriaForm, LancamentosForm
from django.http import JsonResponse


def lancamentos(request):
	#id do usuario logado
	saldo = 0
	id_user = request.user.id
	template = 'caixa/caixa.html'
	lancamentos = LancamentosCaixa.objects.filter(user_id = id_user)
	contexto = {'lancamentos': lancamentos}

	l = LancamentosCaixa.objects.all()


	for l in lancamentos:
		print (l.data)
		print (l.categoria)
		
		if (l.categoria.tipo == '1'):
			saldo += l.valor
		else:
			saldo -= l.valor
		print (l.valor)
		print ("seu saldo atual é "+ str(saldo))

	return render(request, template, contexto)

def categoria(request):
	template = 'caixa/categoria.html'
	catEntrada = Categoria.objects.filter(tipo = 1)
	catSaida = Categoria.objects.filter(tipo = 2)
	
	if(request.method == 'POST'):
		form = CategoriaForm(request.POST)
		if(form.is_valid()):
			form.save()
			return HttpResponseRedirect('/caixa/categoria')

	else:
		form = CategoriaForm()

	contexto = {'catEntrada': catEntrada, 'catSaida': catSaida, 'form': form}

	return render(request, template, contexto)

def editLancamento(request):

	if(request.method == 'POST'):
		#id do lancamento clicado
		idLancamento = request.POST.get('id')
		#busca o lancamento a ser alterado
		lancamento = LancamentosCaixa.objects.get(pk = idLancamento)
		#atribui o lancamento ao form	
		form = LancamentosForm(request.POST, instance = lancamento)

		if(form.is_valid()):
			form.save()
			return HttpResponse("Formulário alterado com sucesso")
		else:
			return HttpResponse("Formulário inválido")

	#id do lancamento clicado
	idLancamento = request.GET.get('id')
	lancamento = LancamentosCaixa.objects.get(pk = idLancamento)
	form = LancamentosForm(instance = lancamento)

	#retorna o id do lancamento junto com o formulario
	divId = "<div id='id_lancamento'>" + idLancamento + "</div>"

	form_html = {form.as_p(), divId}
	return HttpResponse(form_html)


def delLancamento(request):
	if(request.method == 'POST'):
		#id do lancamento a ser deletado
		idLancamento = request.POST.get('id')

		#busca o lançamento
		lancamento = LancamentosCaixa.objects.get(pk = idLancamento)		
		
		if(request.user.id == lancamento.user_id):
			lancamento.delete()
			return HttpResponse("Lançamento excluído com sucesso")
		else:
			return HttpResponse("Lançamento não encontrado.")
		

	return HttpResponse("Lançamento não encontrado.")

	
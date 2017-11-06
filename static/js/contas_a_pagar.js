$(function() {
	var csrftokenGET = getCookie('csrftoken');
	var csrftokenPOST = getCookie('csrftoken');
	//funcao criada para gerar o csrftoken no envio da requisicao POST para o Django
	function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}


	$('.openEdit').on('click', function() {
		//atribui o id do lancamento a variavel
		var id = $(this).attr('data-lanc');
		//envia a solicitacao do formulario com o id do lancamento via ajax
		$.ajax({
			type: 'GET',
			url: '/contas_a_pagar/edit/',
			data: {'id': id, 'csrfmiddlewaretoken': csrftokenGET},
			success: function(contaAPagar) {

				//insere o form vindo do django na div editContPag
				$('#editContPag').html(contaAPagar);

				//Atribui o id do lancamento a uma tag e remove a div vinda do Django
				var id_contaAPagar = $('#id_contaAPagar').html();
				$('#datepickerCP_edit').attr('data-cp', id_contaAPagar);
				$('#id_contaAPagar').remove();

				var data = $("#datepickerCP_edit").val();
				dia = data.substring(8);
				mes = data.substring(5, 7);
				ano = data.substring(0, 4)
				newData = dia + "/" + mes + "/" + ano
				//alterar a data para o formato brasileiro o lancamento carregado
				$("#datepickerCP_edit").val(newData);

				//alterar para o formato brasileiro
				$("#datepickerCP_edit").datepicker({
                    dateFormat: 'dd/mm/yy',
                    dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'],
                    dayNamesMin: ['D','S','T','Q','Q','S','S','D'],
                    dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],
                    monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
                    monthNamesShort: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'],
                    nextText: 'Próximo',
                    prevText: 'Anterior'
                });
				$('#editContasPagar').modal('show');
			},
			error: function(erro) {
				console.log(erro.responseText);
				alert("Lançamento não encontrado. Tente novamente.");
			},

		});
	});

	$('.salvar').click(function(evento) {
		evento.preventDefault();
		
		//recupera os valores dos campos e converte para o formato Json
		var dados = recuperCampos();
		console.log(dados);

		$.ajax({
			type: 'POST',
			url: '/contas_a_pagar/edit/',
			data: dados,
			success: function(msg) {
				//mensagem de confirmação
				alert(msg);
				//recarregar pagina
				location.reload();
			},
			error: function(msg) {
				alert(msg);
			},
		});		
	});

	$('.excluir').click(function(evento) {
		evento.preventDefault();

		if(confirm("Tem certeza que deseja excluir o lançamento?")) {
			var dados = recuperCampos();
			$.ajax({
				type: 'POST',
				url: 'delete/',
				data: dados,
				success: function(msg) {
					//mensagem de confirmação
					alert(msg);
					//recarregar pagina
					location.reload();
				},
				error: function(msg) {
					//mensagem de retorno em caso de erro
					alert(msg)
				},
			});
		}
	});

	function recuperCampos() {
		var id = $('#datepickerCP_edit').attr('data-cp');
		var data = $('#datepickerCP_edit').val();
		var categoria = $('#id_categoria_edit').val();
		var descricao = $('#id_descricao_edit').val();
		var valor = $('#id_valor_edit').val();

		dados = {
			'id': id,
			'data': data,
			'categoria': categoria,
			'descricao': descricao,
			'valor': valor,
			'csrfmiddlewaretoken': csrftokenPOST
		}
		return dados;
	}

});
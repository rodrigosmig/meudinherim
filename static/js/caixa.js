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
			url: '/caixa/edit/',
			data: {'id': id, 'csrfmiddlewaretoken': csrftokenGET},
			success: function(lancamento) {
				//insere o form vindo do django na div editLanc
				$('#editLanc').html(lancamento);

				//Atribui o id do lancamento a uma tag e remove a div vinda do Django
				var id_lancamento = $('#id_lancamento').html();
				$('#datepicker').attr('data-lanc', id_lancamento);
				$('#id_lancamento').remove();

				var data = $("#datepicker").val();
				dia = data.substring(8);
				mes = data.substring(5, 7);
				ano = data.substring(0, 4)
				newData = dia + "/" + mes + "/" + ano
				//alterar a data para o formato brasileiro o lancamento carregado
				$("#datepicker").val(newData);

				//alterar para o formato brasileiro
				$("#datepicker").datepicker({
                    dateFormat: 'dd/mm/yy',
                    dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'],
                    dayNamesMin: ['D','S','T','Q','Q','S','S','D'],
                    dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],
                    monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
                    monthNamesShort: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'],
                    nextText: 'Próximo',
                    prevText: 'Anterior'
                });
				$('#editLancamento').modal();
			},
			error: function(erro) {
				console.log(erro.responseText);
				alert("Lançamento não encontrado. Tente novamente.");
			},

		});
	});

	$('.salvar').click(function() {
		//atribui o id do lancamento a variavel
		var id = $('#datepicker').attr('data-lanc');

		var data = $('#datepicker').val();
		var categoria = $('#id_categoria').val();
		var descricao = $('#id_descricao').val();
		var valor = $('#id_valor').val();

		var dados = {
				'id': id,
				'data': data,
				'categoria': categoria,
				'descricao': descricao,
				'valor': valor,
				'csrfmiddlewaretoken': csrftokenPOST
			}

		// $.post('/caixa/edit/', dados).done(function(msg) {
		// 	alert(msg + " acerto");
		// }).fail(function(msg) {
		// 	alert(msg + " erro");
		// });

		$.ajax({
			type: 'POST',
			url: '/caixa/edit/',
			data: {
				'id': id,
				'data': data,
				'categoria': categoria,
				'descricao': descricao,
				'valor': valor,
				'csrfmiddlewaretoken': csrftokenPOST
			},
			dataType: 'json',
			success: function(msg) {
				console.log(msg);
			},
			error: function(msg) {
				console.log(msg);
			},
		});		
	});

}) 
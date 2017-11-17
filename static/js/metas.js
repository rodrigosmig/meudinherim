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

	$(document).on('click', '.openEdit', function() {
		//atribui o id da meta a variavel
		var id = $(this).attr('data-meta');
		//envia a solicitacao do formulario com o id da meta via ajax
		$.ajax({
			type: 'GET',
			url: '/metas/edit/',
			data: {'id': id, 'csrfmiddlewaretoken': csrftokenGET},
			success: function(meta) {
				//insere o form vindo do django na div editMetaForm
				$('#editMetaForm').html(meta);

				//Atribui o id da meta a uma tag e remove a div vinda do Django
				var id_meta = $('#id_meta').html();
				$('#datepickerMI-alter_meta').attr('data-meta', id_meta);
				$('#id_meta').remove();

				var data = $("#datepickerMI-alter_meta").val();
				dia = data.substring(8);
				mes = data.substring(5, 7);
				ano = data.substring(0, 4)
				dataInicio = dia + "/" + mes + "/" + ano
				//alterar a data para o formato brasileiro a meta carregada
				$("#datepickerMI-alter_meta").val(dataInicio);

				var data = $("#datepickerMF-alter_meta").val();
				dia = data.substring(8);
				mes = data.substring(5, 7);
				ano = data.substring(0, 4)
				dataFim = dia + "/" + mes + "/" + ano
				//alterar a data para o formato brasileiro a meta carregada
				$("#datepickerMF-alter_meta").val(dataFim);

				//alterar para o formato brasileiro
				$("#datepickerMI-alter_meta").datepicker({
                    dateFormat: 'dd/mm/yy',
                    dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'],
                    dayNamesMin: ['D','S','T','Q','Q','S','S','D'],
                    dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],
                    monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
                    monthNamesShort: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'],
                    nextText: 'Próximo',
                    prevText: 'Anterior'
                });

                $("#datepickerMF-alter_meta").datepicker({
                    dateFormat: 'dd/mm/yy',
                    dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'],
                    dayNamesMin: ['D','S','T','Q','Q','S','S','D'],
                    dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],
                    monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
                    monthNamesShort: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'],
                    nextText: 'Próximo',
                    prevText: 'Anterior'
                });
			},
			error: function(erro) {
				console.log(erro.responseText);
				alert("Lançamento não encontrado. Tente novamente.");
			},

		});
	});

	$('.salvar').click(function(evento) {
		
		evento.preventDefault();
		
		var dados = recuperCampos();
		console.log(dados);

		$.ajax({
			type: 'POST',
			url: '/metas/edit/',
			data: dados,
			success: function(msg) {
				//mensagem de confirmação
				alert(msg);
				//recarregar pagina
				location.reload();
			},
			error: function(msg) {
				alert('Dados inválidos. Tente novamente');
			},
		});		
	});

	function recuperCampos() {
		var id = $('#datepickerMI-alter_meta').attr('data-meta');
		var dataInicio = $('#datepickerMI-alter_meta').val();
		var dataFim = $('#datepickerMF-alter_meta').val();
		var titulo = $('#id_titulo-alter_meta').val();
		var valor = $('#id_valor-alter_meta').val();

		dados = {
			'id': id,
			'dataInicio': dataInicio,
			'dataFim': dataFim,
			'titulo': titulo,
			'valor': valor,
			'csrfmiddlewaretoken': csrftokenPOST
		}
		return dados;
	}

	$('.excluir').click(function(evento) {
		evento.preventDefault();

		if(confirm("Tem certeza que deseja excluir a meta?")) {
			var dados = recuperCampos();
			$.ajax({
				type: 'POST',
				url: '/metas/delete/',
				data: dados,
				success: function(msg) {
					//mensagem de confirmação
					alert(msg);
					//recarregar pagina
					location.reload();
				},
				error: function(msg) {
					//mensagem de retorno em caso de erro
					alert("Meta não encontrada.")
				},
			});
		}
	});

});
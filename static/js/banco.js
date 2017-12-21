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

		$.ajax({
			type: 'GET',
			url: '/banco/edit/',
			data: {'id': id, 'csrfmiddlewaretoken': csrftokenGET},
			success: function(lancamento) {
				//insere o form vindo do django na div editLanc
				$('#editLanc').html(lancamento);

				//Atribui o id do lancamento a uma tag e remove a div vinda do Django
				var id_lancamento = $('#id_lancamento').html();
				$('#datepicker-alter_banco').attr('data-lanc', id_lancamento);
				$('#id_lancamento').remove();

				var data = $("#datepicker-alter_banco").val();
				dia = data.substring(8);
				mes = data.substring(5, 7);
				ano = data.substring(0, 4)
				newData = dia + "/" + mes + "/" + ano
				//alterar a data para o formato brasileiro o lancamento carregado
				$("#datepicker-alter_banco").val(newData);

				//diminui o tamanho do input
				$('#id_banco').css('width', '150');

				$("#datepicker-alter_banco").datepicker({
                    dateFormat: 'dd/mm/yy',
                    dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'],
                    dayNamesMin: ['D','S','T','Q','Q','S','S','D'],
                    dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],
                    monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
                    monthNamesShort: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'],
                    nextText: 'Próximo',
                    prevText: 'Anterior'
                });
				$('#editLancamento').modal('show');
			},
			error: function(erro) {
				console.log(erro.responseText);
				alert("Lançamento não encontrado. Tente novamente.");
			},
		});

	});

	$('#form_lancamento_banco').on('submit', function(evento) {
		evento.preventDefault();
		
		var dados = recuperCampos();

		$.ajax({
			type: 'POST',
			url: '/banco/edit/',
			data: dados,
			success: function(msg) {
				//mensagem de confirmação
				$.alert({
					title: false,
					content: msg,
					theme: 'material',
					onClose: function() {
						//recarrega a página
						location.reload();
					}
				});
			},
			error: function(msg) {
				$.alert(msg.responseText);
			},
		});
	});

	$('.excluir').click(function(evento) {
		evento.preventDefault();
		var dados = recuperCampos();
		//verificar se o lançamento foi gerado pelo contas a pagar
		$.ajax({
			type: 'POST',
			url: 'verificar/',
			data: {
				'id': dados.id,
				'csrfmiddlewaretoken': csrftokenPOST,
			},
			success: function(id_lancamento) {
				$.confirm({
					title: 'Excluir lançamento!',
				    content: 'Tem certeza que deseja excluir o lançamento?',
				    draggable: true,
				    theme: 'material',
				    buttons: {
				    	Sim: function() {
				    		$.ajax({
								type: 'POST',
								url: 'delete/',
								data: dados,
								success: function(msg) {
									//mensagem de confirmação
									$.alert({
										title: false,
										content: msg,
										theme: 'material',
										onClose: function() {
											//recarrega a página
											location.reload();
										}
									});	
								},
								error: function(msg) {
									//mensagem de retorno em caso de erro
									$.alert(msg.responseText);
								},
							});
				    	},
				    	Não: function() {},
				    }
				});
			},
			error: function(msg) {
				//mensagem de retorno em caso de erro
				$.alert(msg.responseText);
			},
		});
		
	});

	function recuperCampos() {
		var id = $('#datepicker-alter_banco').attr('data-lanc');
		var banco = $('#id_banco-alter_banco').val();
		var data = $('#datepicker-alter_banco').val();
		var tipo = $('#id_tipo-alter_banco').val();
		var categoria = $('#id_categoria-alter_banco').val();
		var descricao = $('#id_descricao-alter_banco').val();
		var valor = $('#id_valor-alter_banco').val();

		dados = {
			'id': id,
			'banco': banco,
			'data': data,
			'tipo': tipo,
			'categoria': categoria,
			'descricao': descricao,
			'valor': valor,
			'csrfmiddlewaretoken': csrftokenPOST
		}
		return dados;
	}

});
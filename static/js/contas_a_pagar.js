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
		var id = $(this).attr('data-cp');
		//envia a solicitacao do formulario com o id da conta via ajax
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
				$.alert("Lançamento não encontrado. Tente novamente.");
			},

		});
	});

	$('#form_cadastro_pagar').on('submit', function(evento) {
		evento.preventDefault();
		
		var data = $('#datepickerCP').val();
		var categoria = $('#id_categoriaCP').val();
		var descricao = $('#id_descricaoCP').val();
		var valor = $('#id_valorCP').val();

		$.ajax({
			type: 'POST',
			url: '/contas_a_pagar/',
			data: {
				'data': data,
				'categoria': categoria,
				'descricao': descricao,
				'valor': valor,
				'csrfmiddlewaretoken': csrftokenPOST,
			},
			success: function(msg) {
				$('#contas_a_pagar').modal('hide');
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
				$('#datepickerCP').val("");
				$('#id_categoriaCP').val("");
				$('#id_descricaoCP').val("");
				$('#id_valorCP').val("");

			},
			error: function(msg) {
				$.alert(msg.responseText);
			},
		});		
	});

	$('.salvar').click(function(evento) {
		evento.preventDefault();
		
		//recupera os valores dos campos e converte para o formato Json
		var dados = recuperCampos();

		$.ajax({
			type: 'POST',
			url: '/contas_a_pagar/edit/',
			data: dados,
			success: function(msg) {
				$('#editContasPagar').modal('hide');
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
		$.ajax({
    		type: 'POST',
			url: 'verificar/',
			data: {
				'id': dados.id,
				'csrfmiddlewaretoken': csrftokenPOST,
			},
			success: function(id_pagamento) {
				$.confirm({
				    title: 'Excluir pagamento!',
				    content: 'Tem certeza que deseja excluir o pagamento?',
				    draggable: true,
				    theme: 'material',
				    buttons: {
				        Sim: function() {
				        	$.ajax({
				        		type: 'POST',
								url: 'delete/',
								data: {
									'id': id_pagamento,
									'csrfmiddlewaretoken': csrftokenPOST,
								},
								success: function(msg) {
									$('#editContasPagar').modal('hide');
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
				        	})
				        },
				        Não: function() {},
				    }
				});
			},
			error: function(msg) {
				//mensagem de retorno em caso de erro
				$.alert(msg.responseText)
			},
    	})
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

	$('#pagamentoConta').on('hidden.bs.modal', function () {
    	$('#campos_conta').empty();
    	$('#carteira').prop("checked", true);
    	$('#campos_conta .label_conta').remove();
	})

	$('.openPay').on('click', function() {
		//armazena o id da conta para pegar os valores cadastrados
		var id = $(this).attr('data-cp');
		$('.pagar').attr('data-cp', id);

		id = '#' + id

		//esconde o select-box
		$('#select_bancos').hide();

		var data = $(id).children('.conta_data').html();
		var id_cat = $(id).children('.conta_cat').attr('data-id_cat');
		var categoria = $(id).children('.conta_cat').html();
		var descricao = $(id).children('.conta_desc').html();
		var valor = $(id).children('.conta_val').html();
		
		//inserir os campos de acordo com a conta clicada
		var campos = $('#campos_conta');
		campos.append($("<label />").text("Data:"));
		campos.append($("<input type='text'>").addClass("form-control").prop('disabled', true).prop('id', 'data_pagam').val(data));

		campos.append($("<label />").text("Categoria:"));
		campos.append($("<input type='text'>").addClass("form-control").prop('disabled', true).prop('id', 'cat_pagam').val(categoria));

		campos.append($("<label />").text("Descrição:"));
		campos.append($("<input type='text'>").addClass("form-control").prop('disabled', true).prop('id', 'desc_pagam').val(descricao));

		campos.append($("<label />").text("Valor:"));
		campos.append($("<input type='text'>").addClass("form-control").prop('disabled', true).prop('id', 'val_pagam').val(valor));
	});

	$('.cancelPay').on('click', function() {
		var id_pagamento = $(this).attr('data-cp');

		$.confirm({
		    title: 'Cancelar pagamento!',
		    content: 'Tem certeza que deseja cancelar o pagamento?',
		    draggable: true,
		    theme: 'material',
		    buttons: {
		        Sim: function () {
		        	$.ajax({
		        		type: 'POST',
						url: '/contas_a_pagar/cancelar/',
						data: {
							'id': id_pagamento,
							'csrfmiddlewaretoken': csrftokenPOST,
						},
						success: function(msg) {
							//mensagem de confirmação
							$.alert({
								title: false,
								theme: 'material',
								content: msg + ' O lançamento gerado pelo pagamento foi excluído.',
    							onClose: function() {
    								//recarrega a página
    								location.reload();
    							}
							});						
						},
						error: function(msg) {
							//mensagem de retorno em caso de erro
							$.alert(msg.responseText)
						},
		        	})
		        },
		        Não: function() {},
		    }
		});		
	});


	$('.conta_select').on('change', function() {
		var tipo = $(this).attr('data-tipo');
		if(tipo === 'caixa') {
			$('#select_bancos').remove();
			$('#campos_conta .label_conta').remove();
		}
		else {
			$('#campos_conta').prepend($('<select />').addClass("form-control").attr('id', 'select_bancos'))
			$('#campos_conta').prepend($('<label />').addClass('label_conta').prop('for', 'select_bancos').text("Conta:"));
			$.ajax({
				type: 'POST',
				url: '/contas_a_pagar/banco/',
				data: {'csrfmiddlewaretoken': csrftokenPOST},
				datatype: 'json',
				success: function(bancos) {

					$.each(bancos, function (i, banco) {
					    $('#select_bancos').append($('<option>', { 
					        value: banco.fields.banco,
					        text : banco.fields.banco
					    }).attr('value', banco.fields.banco));
					});

					//mostra o select-box
					$('#select_bancos').show();
				},
				error: function(bancos) {
					console.log(banco);
				},
			});	
		}
	});

	$('.pagar').click(function(evento) {
		evento.preventDefault();

		var banco = $('#select_bancos').val();
		if(banco === undefined) {
			banco = "";
		}

		var id = $(this).attr('data-cp');
		
		$.ajax({
			type: 'POST',
			url: '/contas_a_pagar/pagar/',
			data: {
				'id': id, 
				'banco': banco,
				'csrfmiddlewaretoken': csrftokenPOST
			},
			success: function(msg) {
				$('#pagamentoConta').modal('hide');
				//mensagem de confirmação
				$.alert({
					title: false,
					theme: 'material',
					content: msg,
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

});
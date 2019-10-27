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
		//atribui o id do lancamento a variavel
		var id = $(this).attr('data-cp');
		//envia a solicitacao do formulario com o id da conta via ajax
		$.ajax({
			type: 'GET',
			url: '/contas_a_pagar/edit/',
			data: {'id_contas_a_pagar': id, 'csrfmiddlewaretoken': csrftokenGET},
			success: function(contaAPagar) {

				//insere o form vindo do django na div editContPag
				$('#editContPag').html(contaAPagar);

				//Atribui o id do lancamento a uma tag e remove a div vinda do Django
				var id_contaAPagar = $('#id_contaAPagar').html();
				$('#id_contas_a_pagar-alter_CP').val(id_contaAPagar);
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
				$.alert({
					title: false,
					content: erro.responseText,
					theme: 'material',
					onClose: function() {
						$("#editContasPagar").modal('hide')
					}
				});			
			},

		});
	});

	$('.excluir').click(function(evento) {
		evento.preventDefault();
		var id = $("#id_contas_a_pagar-alter_CP").val()

		$.ajax({
    		type: 'POST',
			url: 'verificar/',
			data: {
				'id_contas_a_pagar': id,
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
							$('#form_edit_CP').attr('action', '/contas_a_pagar/delete/')
							$('#form_edit_CP').submit()
				        },
				        Não: function() {},
				    }
				});
			},
			error: function(msg) {
				$.alert(msg.responseText)
			},
    	})
	});

	$('#pagamentoConta').on('hidden.bs.modal', function () {
    	$('#campos_conta').empty();
    	$('#carteira').prop("checked", true);
    	$('#campos_conta .label_conta').remove();
	})

	$(document).on('click', '.openPay', function() {
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
		campos.append($("<input type='text'>").addClass("form-control").prop('disabled', true).prop('id', 'data_vencimento').val(data));

		campos.append($("<label />").text("Data de pagamento:"));
		campos.append($("<input type='text'>").addClass("form-control").prop('id', 'data_pagamento'));

		campos.append($("<label />").text("Categoria:"));
		campos.append($("<input type='text'>").addClass("form-control").prop('disabled', true).prop('id', 'cat_pagam').val(categoria));

		campos.append($("<label />").text("Descrição:"));
		campos.append($("<input type='text'>").addClass("form-control").prop('disabled', true).prop('id', 'desc_pagam').val(descricao));

		campos.append($("<label />").text("Valor:"));
		campos.append($("<input type='text'>").addClass("form-control").prop('disabled', true).prop('id', 'val_pagam').val(valor));
		
		$("#data_pagamento").datepicker({
			dateFormat: 'dd/mm/yy',
			dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'],
			dayNamesMin: ['D','S','T','Q','Q','S','S','D'],
			dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],
			monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
			monthNamesShort: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'],
			nextText: 'Próximo',
			prevText: 'Anterior'
		});
	});

	$(document).on('click', '.cancelPay', function() {
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
							'id_contas_a_pagar': id_pagamento,
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
					        value: banco.pk,
					        text : banco.fields.banco
					    }).attr('value', banco.pk));
					});

					$('#select_bancos').show();
				},
				error: function(bancos) {

				},
			});	
		}
	});

	$('.pagar').click(function(evento) {
		evento.preventDefault();
		
		if($("#data_pagamento").val() == "") {
			$.alert({
				title: false,
				theme: 'material',
				content: "Informe a data de pagamento!",
			});	
		}
		else {
			var banco = $('#select_bancos').val();
			if(banco === undefined) {
				banco = "";
			}

			var id 			= $(this).attr('data-cp');
			var pagamento 	= $("#data_pagamento").val()
			
			$.ajax({
				type: 'POST',
				url: '/contas_a_pagar/pagar/',
				data: {
					'id_contas_a_pagar': id, 
					'id_banco': banco,
					'data_pagamento': dataConvert(pagamento),
					'csrfmiddlewaretoken': csrftokenPOST
				},
				success: function(msg) {
					$('#pagamentoConta').modal('hide');
					$.alert({
						title: false,
						theme: 'material',
						content: msg,
						onClose: function() {
							location.reload();
						}
					});	
				},
				error: function(msg) {
					$.alert(msg.responseText);
				},
			});
		}
	});

	function dataConvert(data) {
		data_array = data.split("/")
		new_data = data_array[2] + "-" + data_array[1] + "-" + data_array[0]
		return new_data
	}

	$('#form_filtro_cp').on('submit', function(evento) {
		evento.preventDefault();

		var mes = $('#filter_mes_cp').val();
		var ano = $('#filter_ano_cp').val();
		var status = $('#filter_status_cp').val();

		if(mes === 'nenhum' || status ==='nenhum' || ano === 'nenhum') {
			$.alert('Selecione o mês, o ano e o status desejado.');
		}
		else {
			mes = parseInt(mes) + 1
			$.ajax({
	    		type: 'POST',
				url: '/contas_a_pagar/filtrar/',
				data: {
					'mes': mes,
					'ano': ano,
					'status': status,
					'csrfmiddlewaretoken': csrftokenGET,
				},
				success: function(contas) {
					var table = $('#dataBanco').DataTable();

					var rows = table.clear().draw();

					for(var x = 0; x < contas.length; x++) {
						var paga;
						var edit
						
						if(contas[x].fields.paga === false) {
							paga = "<i class='material-icons'><a data-toggle='modal' href='#pagamentoConta' style='color: red' title='Clique para pagar'><span class='openPay' data-cp=" + contas[x].pk + ">close</span></a></i>"
							edit = "<i class='material-icons'><a data-toggle='modal' href='#editContasPagar' title='Clique para editar'><span class='openEdit' data-cp=" + contas[x].pk + ">edit</span></a></i>"
						}
						else {
							paga = "<i class='material-icons pago'><span class='cancelPay' data-cp=" + contas[x].pk + "><a data-toggle='modal' href='' title='Clique para cancelar o pagamento'>done</span></i>"
							edit = "<i class='material-icons'><a title='Cancele o pagamento para editar'><span data-cp=" + contas[x].pk + ">edit</span></a></i>"
						}

						var data_vencimento = convertData(contas[x].fields.data);
						var data_pagamento
						if(contas[x].fields.data_pagamento == null) {
							if(contas[x].fields.paga == true) {
								data_pagamento = convertData(contas[x].fields.data)
							}
							else {
								data_pagamento = ""
							}
							
						}
						else {
							data_pagamento = convertData(contas[x].fields.data_pagamento)
						}
	
						var row = table.row.add([
							data_vencimento,
							data_pagamento,
							contas[x].fields.descricao,
							contas[x].fields.categoria[2],
							contas[x].fields.valor.replace('.', ','),
							edit,
							paga,
						]);
						//adiciona o id do pagamento na linha
						table.row(row).node().id = contas[x].pk;
						//adiciona as classes da tag html
						table.row(row).column(0).nodes().to$().addClass('conta_data');
						table.row(row).column(1).nodes().to$().addClass('conta_desc');
						table.row(row).column(2).nodes().to$().addClass('conta_cat');
						table.row(row).column(3).nodes().to$().addClass('conta_val');
						table.row(row).draw(false);
					}
											
				},
				error: function(msg) {
					//mensagem de retorno em caso de erro
					$.alert(msg.responseText)
				},
	    	})
		}

		
	});

	function convertData(data) {
		dia = data.substring(8);
		mes = data.substring(5, 7);
		ano = data.substring(0, 4);
		newData = dia + "/" + mes + "/" + ano;
		return newData
	}

});
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

	setDateinSelect()

	function setYear(year) {
		for (let ano = 2017; ano <= year + 1; ano++) {
			$("#filter_ano_cr").append("<option value=" + ano + ">" + ano + "</option>")			
		}
	}

	function setDateinSelect() {
		var data = new Date();
		var mesAtual = data.getMonth();
		var anoAtual = data.getFullYear();

		setYear(anoAtual)

		$('#filter_mes_cr').val(mesAtual).prop('selected', true);
		$('#filter_ano_cr').val(anoAtual).prop('selected', true);

	}

	$(document).on('click', '.openEdit', function() {
		setWaitMe("editContasReceber")
		var id = $(this).attr('data-cr');
		$.ajax({
			type: 'GET',
			url: '/contas_a_receber/edit/',
			data: {'id_contas_a_receber': id, 'csrfmiddlewaretoken': csrftokenGET},
			success: function(contaAReceber) {
				$('#editContRec').html(contaAReceber);
				
				hideWaitMe('editContasReceber')
				
				var id_contaAReceber = $('#id_contaAReceber').html();
				$('#id_contas_a_receber-alter_CR').val(id_contaAReceber);
				$('#id_contaAReceber').remove();

				var data = $("#datepickerCR_edit").val();
				dia = data.substring(8);
				mes = data.substring(5, 7);
				ano = data.substring(0, 4)
				newData = dia + "/" + mes + "/" + ano
				//alterar a data para o formato brasileiro o lancamento carregado
				$("#datepickerCR_edit").val(newData);

				//alterar para o formato brasileiro
				$("#datepickerCR_edit").datepicker({
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
						$("#editContasReceber").modal('hide')
					}
				});			
			},

		});
	});

	$('#form_cadastro_receber').on('submit', function(evento) {
		evento.preventDefault();
		setWaitMe("mod_add_contas_a_receber")
		evento.currentTarget.submit()
	});

	$('#form_edit_receber').on('submit', function(evento) {
		evento.preventDefault();
		setWaitMe("editContasReceber")
		evento.currentTarget.submit()
	});

	$('.excluir').click(function(evento) {
		evento.preventDefault();
		var id = $("#id_contas_a_receber-alter_CR").val()

		$.ajax({
    		type: 'POST',
			url: 'verificar/',
			data: {
				'id_contas_a_receber': id,
				'csrfmiddlewaretoken': csrftokenPOST,
			},
			success: function(id_recebimento) {
				$.confirm({
				    title: 'Excluir a conta!',
				    content: 'Tem certeza que deseja excluir a conta?',
				    draggable: true,
				    theme: 'material',
				    buttons: {
				        Sim: function() {
							$('#form_edit_receber').attr('action', '/contas_a_receber/delete/')
							$('#form_edit_receber').submit()
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

	$('#recebimentoConta').on('hidden.bs.modal', function () {
    	$('#campos_conta').empty();
    	$('#carteira').prop("checked", true);
    	$('#campos_conta .label_conta').remove();
	})

	$(document).on('click', '.openReceive', function() {
		$('#carteira').prop("checked", true);
		//armazena o id da conta para pegar os valores cadastrados
		var id = $(this).attr('data-cr');
		$('.receber').attr('data-cr', id);

		id = '#' + id;

		//esconde o select-box do banco
		$('#select_bancos').hide();

		var data = $(id).children('.conta_data').html();
		var id_cat = $(id).children('.conta_cat').attr('data-id_cat');
		var categoria = $(id).children('.conta_cat').html();
		var descricao = $(id).children('.conta_desc').html();
		var valor = $(id).children('.conta_val').html();
		
		//inserir os campos de acordo com a conta clicada
		var campos = $('#campos_conta');
		campos.append($("<label />").text("Data de vencimento:"));
		campos.append($("<input type='text'>").addClass("form-control").prop('disabled', true).prop('id', 'data_vencimento').val(data));

		campos.append($("<label />").text("Data do recebimento:"));
		campos.append($("<input type='text'>").addClass("form-control").prop('id', 'data_recebimento'));

		campos.append($("<label />").text("Categoria:"));
		campos.append($("<input type='text'>").addClass("form-control").prop('disabled', true).prop('id', 'cat_pagam').val(categoria));

		campos.append($("<label />").text("Descrição:"));
		campos.append($("<input type='text'>").addClass("form-control").prop('disabled', true).prop('id', 'desc_pagam').val(descricao));

		campos.append($("<label />").text("Valor:"));
		campos.append($("<input type='text'>").addClass("form-control").prop('disabled', true).prop('id', 'val_pagam').val(valor));

		$("#data_recebimento").datepicker({
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


	//retorna json com os agencias bancarias do usuário
	$('.conta_select').on('change', function() {
		var tipo = $(this).attr('data-tipo');
		if(tipo === 'caixa') {
			$('#select_bancos').remove();
			$('#campos_conta .label_conta').remove();
		}
		else {
			$('#campos_conta').prepend($('<select />').addClass("form-control").attr('id', 'select_bancos'))
			$('#campos_conta').prepend($('<label />').addClass('label_conta').prop('for', 'select_bancos').text("Agência:"));
			$.ajax({
				type: 'POST',
				url: '/contas_a_pagar/banco/',
				data: {'csrfmiddlewaretoken': csrftokenPOST},
				datatype: 'json',
				success: function(bancos) {
					//cria o select box com as agencias
					$.each(bancos, function (i, banco) {
					    $('#select_bancos').append($('<option>', {
							value: banco.pk,
					        text : banco.fields.banco
					    }).attr('value', banco.pk));
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

	$('.receber').on('click', function(evento) {
		evento.preventDefault();
		
		if($("#data_recebimento").val() == "") {
			$.alert({
				title: false,
				theme: 'material',
				content: "Informe a data do recebimento!",
			});	
		}
		else {
			setWaitMe("recebimentoConta")
			var banco = $('#select_bancos').val();
			if(banco === undefined) {
				banco = "";
			}

			var id = $(this).attr('data-cr');
			var recebimento = $("#data_recebimento").val()

			$.ajax({
				type: 'POST',
				url: '/contas_a_receber/receber/',
				data: {
					'id_contas_a_receber': id, 
					'banco': banco,
					'data_recebimento': dataConvert(recebimento),
					'csrfmiddlewaretoken': csrftokenPOST
				},
				success: function(msg) {
					hideWaitMe("recebimentoConta")
					$('#recebimentoConta').modal('hide');
					//mensagem de confirmação
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
					hideWaitMe("recebimentoConta")
				},
			});
		}

		function dataConvert(data) {
			data_array = data.split("/")
			new_data = data_array[2] + "-" + data_array[1] + "-" + data_array[0]
			return new_data
		}
				
	});

	$(document).on('click', '.cancelReceive', function() {
		var id_pagamento = $(this).attr('data-cr');

		$.confirm({
		    title: 'Cancelar recebimento!',
		    content: 'Tem certeza que deseja cancelar o recebimento?',
		    draggable: true,
		    theme: 'material',
		    buttons: {
		        Sim: function () {
		        	$.ajax({
		        		type: 'POST',
						url: '/contas_a_receber/cancelar/',
						data: {
							'id_contas_a_receber': id_pagamento,
							'csrfmiddlewaretoken': csrftokenPOST,
						},
						success: function(msg) {
							//mensagem de confirmação
							$.alert({
								title: false,
								theme: 'material',
								content: msg + ' O lançamento gerado pelo recebimento foi excluído.',
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

	$('#form_filtro_cr').on('submit', function(evento) {
		evento.preventDefault();
		setWaitMe("card_principal")

		var mes = parseInt($('#filter_mes_cr').val()) + 1;
		var ano = $('#filter_ano_cr').val();
		var status = $('#filter_status_cr').val();

		$.ajax({
			type: 'POST',
			url: '/contas_a_receber/filtrar/',
			data: {
				'mes': mes,
				'ano': ano,
				'status': status,
				'csrfmiddlewaretoken': csrftokenGET,
			},
			success: function(contas) {
				var table = $('#dataCR').DataTable();

				var rows = table.clear().draw();

				for(var x = 0; x < contas.length; x++) {
					var recebido;
					var edit;

					if(contas[x].fields.recebido === false) {
						recebido = "<i class='material-icons'><a data-toggle='modal' href='#recebimentoConta' style='color: red' title='Clique para receber'><span class='openReceive' data-cr=" + contas[x].pk + ">close</span></a></i>"
						edit = "<i class='material-icons'><a data-toggle='modal' href='#editContasReceber' title='Clique para editar'><span class='openEdit' data-cr=" + contas[x].pk + ">edit</span></a></i>"
					}
					else {
						recebido = "<i class='material-icons recebido'><span class='cancelReceive' data-cr=" + contas[x].pk + "><a data-toggle='modal' href='' title='Clique para cancelar o recebimento'>done</span></i>"
						edit = "<i class='material-icons'><a title='Cancele o recebimento para editar'><span data-cr=" + contas[x].pk + ">edit</span></a></i>"
					}

					var data_vencimento = convertData(contas[x].fields.data);
					var data_recebimento;
					if(contas[x].fields.data_recebimento == null) {
						if(contas[x].fields.recebido == true) {
							data_recebimento = convertData(contas[x].fields.data)
						}
						else {
							data_recebimento = ""
						}
						
					}
					else {
						data_recebimento = convertData(contas[x].fields.data_recebimento)
					}

					var row = table.row.add([
						data_vencimento,
						data_recebimento,
						contas[x].fields.descricao,
						contas[x].fields.categoria[2],
						contas[x].fields.valor.replace('.', ','),
						edit,
						recebido,
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
				hideWaitMe("card_principal")
			},
			error: function(msg) {
				hideWaitMe("card_principal")
				$.alert(msg.responseText)
			},
		})	
	});

	function hideWaitMe(id) {
		$("#" + id).waitMe("hide");
	}

	function setWaitMe(id) {
		$("#" + id).waitMe({
			effect : 'bounce',
			text : 'Aguarde...',
			bg : "rgba(255,255,255,0.7)",
			color : "#000",
			waitTime : "-1",
			textPos : 'vertical',
		})
	}

	function convertData(data) {
		dia = data.substring(8);
		mes = data.substring(5, 7);
		ano = data.substring(0, 4);
		newData = dia + "/" + mes + "/" + ano;
		return newData
	}

	

});
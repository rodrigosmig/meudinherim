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
		var id = $(this).attr('data-lanc');

		$.ajax({
			type: 'GET',
			url: '/banco/edit/',
			data: {'id': id, 'csrfmiddlewaretoken': csrftokenGET},
			success: function(lancamento) {
				//insere o form vindo do django na div editLanc
				$('#editLanc').html(lancamento);

				//informa se o lançamento foi realizado pelo contas a pagar ou contas a receber
				var statusConta = $('#status_conta').html();
				var status = $('#status').html()

				//altera o id do select
				$('#editLanc #categoria_banco').prop('id', 'id_categoria-alter_banco')

				//desabilita os campos quando o lançamento for feito pelo contas a pagar/receber
				if(statusConta === 'Pago' || statusConta === 'Recebido') {
					$('#status').html(status + " (" + statusConta + ")").css('color', 'red');
					$('#datepicker-alter_banco').prop('disabled', true);
					$('#id_banco-alter_banco').prop('disabled', true);
					$('#id_tipo-alter_banco').prop('disabled', true);
					$('#id_categoria-alter_banco').prop('disabled', true);
					$('#id_descricao-alter_banco').prop('disabled', true);
					$('#id_valor-alter_banco').prop('disabled', true);
					$('#btn_salvar').prop('disabled', true);
				}
				$('#status_conta').remove();
				var status = $('#status').html();

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
				$.alert("Lançamento não encontrado. Tente novamente.");
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

	$('#editLancamento').on('hidden.bs.modal', function () {
    	$('#status').html("");
    	$('#btn_salvar').prop('disabled', false);
	});

	$('#select_agencia').on('change', function() {
		
		if($(this).val() !== 'nenhum') {
			$('.saldoBanco').hide();
			var agencia = $(this).val();

			var data = new Date();
			var mesAtual = data.getMonth();
			var anoAtual = data.getFullYear();

			$('#lanc_meses').val(mesAtual).prop('selected', true);
			$('#lanc_anos').val(anoAtual).prop('selected', true);
			var table = $('#dataBanco').DataTable();

			$.ajax({
				type: 'POST',
				url: '/banco/',
				data: {
					'agencia': agencia,
					'mes': mesAtual + 1,
					'ano': anoAtual,
					'csrfmiddlewaretoken': csrftokenPOST,
				},
				success: function(lancamentos) {
					
					$('#select_data').show();

					//limpa a tabela
					table.clear().draw();
					
					if(lancamentos.length !== 0) {
						for(var x = 0; x < lancamentos.length; x++) {

							//mostrar o saldo da conta
							$('.saldoBanco').each(function() {
								if($(this).attr('data-saldo') === lancamentos[x].fields.banco[1]) {
									$(this).show();	
								}
							});

							data = lancamentos[x].fields.data;
							dia = data.substring(8);
							mes = data.substring(5, 7);
							ano = data.substring(0, 4);
							newData = dia + "/" + mes + "/" + ano;

							if(lancamentos[x].fields.tipo === "1") {
								var valor = "<span style='color: blue' >" + lancamentos[x].fields.valor + "</span>";
							}
							else {
								var valor = "<span style='color: red' >-" + lancamentos[x].fields.valor + "</span>";
							}

							var tipo = "";
							if(lancamentos[x].fields.tipo === '1') {
								tipo = 'Crédito';
							}
							else {
								tipo = 'Débito'
							}

							table.row.add([newData,
							lancamentos[x].fields.descricao,
							tipo,
							lancamentos[x].fields.categoria[2],
							valor,
							"<i class='material-icons'><a data-toggle='modal' href=''><span class='openEdit' data-lanc=" + lancamentos[x].pk + ">edit</span></a></i>"
							]).draw(false);
						}
					}
					else {
						//mostrar o saldo da conta
						$('.saldoBanco').each(function() {
							if($(this).attr('data-saldo') === $('#select_agencia').val()) {
								$(this).show();	
							}
						});						
					}
				},
				error: function(msg) {
					table.clear().draw();
					$('#select_data').show();
					$.alert(msg.responseText)
				},
			});
		}
		else {
			$('#dataBanco').DataTable().clear().draw();
			$('#select_data').hide();
		}
	});

	$('#select_agencia_credito').on('change', function() {
		
		if($(this).val() !== 'nenhum') {
			var agencia = $(this).val();

			var data = new Date();
			var mesAtual = data.getMonth();
			var anoAtual = data.getFullYear();

			$('#lanc_meses_credito').val(mesAtual).prop('selected', true);
			$('#lanc_anos_credito').val(anoAtual).prop('selected', true);
			
			$.ajax({
				type: 'POST',
				url: '/banco/',
				data: {
					'agencia': agencia,
					'mes': mesAtual + 1,
					'ano': anoAtual,
					'csrfmiddlewaretoken': csrftokenPOST,
				},
				success: function(lancamentos) {
					
					$('#select_data_credito').show();

					var table = $('#dataCredito').DataTable();

					//limpa a tabela
					var rows = table.clear().draw();
					
					if(lancamentos.length !== 0) {
						for(var x = 0; x < lancamentos.length; x++) {
							data = lancamentos[x].fields.data;
							dia = data.substring(8);
							mes = data.substring(5, 7);
							ano = data.substring(0, 4);
							newData = dia + "/" + mes + "/" + ano;

							if(lancamentos[x].fields.tipo === "1") {
								var valor = "<span style='color: blue' >" + lancamentos[x].fields.valor + "</span>";
							}
							else {
								var valor = "<span style='color: red' >-" + lancamentos[x].fields.valor + "</span>";
							}

							var tipo = "";
							if(lancamentos[x].fields.tipo === '1') {
								tipo = 'Crédito';
							}
							else {
								tipo = 'Débito'
							}

							table.row.add([newData,
							lancamentos[x].fields.descricao,
							tipo,
							lancamentos[x].fields.categoria[2],
							valor,
							"<i class='material-icons'><a data-toggle='modal' href=''><span class='openEdit' data-lanc=" + lancamentos[x].pk + ">edit</span></a></i>"
							]).draw(false);
						}
					}
				},
				error: function(msg) {
					$('#select_data_credito').show();
					$.alert(msg.responseText)
				},
			});
		}
		else {
			$('#dataCredito').DataTable().clear().draw();
			$('#select_data_credito').hide();
		}
	});


	$('#form_filtro_banco').on('submit', function(evento) {
		evento.preventDefault();

		var agencia = $('#select_agencia').val();
		var mes = $('#lanc_meses').val();
		var ano = $('#lanc_anos').val();

		if(mes === 'nenhum' || ano === 'nenhum') {
			$.alert('Selecione o mês e o ano desejado.');
		}
		else {
			mes = parseInt(mes) + 1
			var table = $('#dataBanco').DataTable();

			$.ajax({
				type: 'POST',
				url: '/banco/',
				data: {
					'agencia': agencia,
					'mes': mes,
					'ano': ano,
					'csrfmiddlewaretoken': csrftokenPOST
				},
				datatype: 'json',
				success: function(lancamentos) {
					table.clear().draw();

					if(lancamentos.length !== 0) {

						for(var x = 0; x < lancamentos.length; x++) {

							data = lancamentos[x].fields.data;
							dia = data.substring(8);
							mes = data.substring(5, 7);
							ano = data.substring(0, 4);
							newData = dia + "/" + mes + "/" + ano;

							if(lancamentos[x].fields.tipo === "1") {
								var categoria = "<span style='color: blue' >" + lancamentos[x].fields.valor + "</span>";
							}else{
								var categoria = "<span style='color: red' >-" + lancamentos[x].fields.valor + "</span>";
							}

							var tipo = "";
							if(lancamentos[x].fields.tipo === '1') {
								tipo = 'Crédito';
							}
							else {
								tipo = 'Débito'
							}

							table.row.add([newData,
							lancamentos[x].fields.descricao,
							tipo,
							lancamentos[x].fields.categoria[2],
							categoria,
							"<i class='material-icons'><a data-toggle='modal' href=''><span class='openEdit' data-lanc=" + lancamentos[x].pk + ">edit</span></a></i>"
							]).draw(false);
						}
					}					
				},
				error: function(msg) {
					table.clear().draw();
					//mensagem de retorno em caso de erro
					$.alert(msg.responseText)
					
				},
			});
		}

		
	});

	$('#form_filtro_credito').on('submit', function(evento) {
		evento.preventDefault();

		var agencia = $('#select_agencia_credito').val();
		var mes = $('#lanc_meses_credito').val();
		var ano = $('#lanc_anos_credito').val();

		if(mes === 'nenhum' || ano === 'nenhum') {
			$.alert('Selecione o mês e o ano desejado.');
		}
		else {
			mes = parseInt(mes) + 1
			var table = $('#dataCredito').DataTable();

			$.ajax({
				type: 'POST',
				url: '/banco/',
				data: {
					'agencia': agencia,
					'mes': mes,
					'ano': ano,
					'csrfmiddlewaretoken': csrftokenPOST
				},
				datatype: 'json',
				success: function(lancamentos) {
					table.clear().draw();					

					if(lancamentos.length !== 0) {

						for(var x = 0; x < lancamentos.length; x++) {

							data = lancamentos[x].fields.data;
							dia = data.substring(8);
							mes = data.substring(5, 7);
							ano = data.substring(0, 4);
							newData = dia + "/" + mes + "/" + ano;

							if(lancamentos[x].fields.tipo === "1") {
								var categoria = "<span style='color: blue' >" + lancamentos[x].fields.valor + "</span>";
							}else{
								var categoria = "<span style='color: red' >-" + lancamentos[x].fields.valor + "</span>";
							}

							var tipo = "";
							if(lancamentos[x].fields.tipo === '1') {
								tipo = 'Crédito';
							}
							else {
								tipo = 'Débito'
							}

							table.row.add([newData,
							lancamentos[x].fields.descricao,
							tipo,
							lancamentos[x].fields.categoria[2],
							categoria,
							"<i class='material-icons'><a data-toggle='modal' href=''><span class='openEdit' data-lanc=" + lancamentos[x].pk + ">edit</span></a></i>"
							]).draw(false);
						}
					}					
				},
				error: function(msg) {
					table.clear().draw();
					//mensagem de retorno em caso de erro
					$.alert(msg.responseText)
					
				},
			});
		}

		
	});

});
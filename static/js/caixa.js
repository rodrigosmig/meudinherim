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
		//envia a solicitacao do formulario com o id do lancamento via ajax
		$.ajax({
			type: 'GET',
			url: '/caixa/edit/',
			data: {
				'id': id, 
				'csrfmiddlewaretoken': csrftokenGET
			},
			success: function(lancamento) {
				//insere o form vindo do django na div editLanc
				$('#editLanc').html(lancamento);

				//informa se o lançamento foi realizado pelo contas a pagar ou contas a receber
				var statusConta = $('#status_conta').html();
				var status = $('#status').html()

				//desabilita os campos quando o lançamento for feito pelo contas a pagar/receber
				if(statusConta === 'Pago' || statusConta === 'Recebido') {
					$('#status').html(status + " (" + statusConta + ")").css('color', 'red');
					$('#datepicker-alter_caixa').prop('disabled', true);
					$('#id_categoria-alter_caixa').prop('disabled', true);
					$('#id_descricao-alter_caixa').prop('disabled', true);
					$('#id_valor-alter_caixa').prop('disabled', true);
					$('#btn_salvar').prop('disabled', true);
				}
				$('#status_conta').remove();
				var status = $('#status').html();

				//Atribui o id do lancamento a uma tag e remove a div vinda do Django
				var id_lancamento = $('#id_lancamento').html();
				$('#datepicker-alter_caixa').attr('data-lanc', id_lancamento);
				$('#id_lancamento').remove();

				var data = $("#datepicker-alter_caixa").val();
				dia = data.substring(8);
				mes = data.substring(5, 7);
				ano = data.substring(0, 4)
				newData = dia + "/" + mes + "/" + ano
				//alterar a data para o formato brasileiro o lancamento carregado
				$("#datepicker-alter_caixa").val(newData);

				//alterar para o formato brasileiro
				$("#datepicker-alter_caixa").datepicker({
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

	$('#form_lancamento_caixa').on('submit', function(evento) {
		
		evento.preventDefault();
		
		var dados = recuperCampos();

		$.ajax({
			type: 'POST',
			url: '/caixa/edit/',
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
		var id = $('#datepicker-alter_caixa').attr('data-lanc');
		var data = $('#datepicker-alter_caixa').val();
		var categoria = $('#id_categoria-alter_caixa').val();
		var descricao = $('#id_descricao-alter_caixa').val();
		var valor = $('#id_valor-alter_caixa').val();

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

	//remove o texto inserido quando for contas a pagar/receber e habilita o botão salvar
	$('#editLancamento').on('hidden.bs.modal', function () {
    	$('#status').html("");
    	$('#btn_salvar').prop('disabled', false);
	});

	$('#card_change').hide();

	//selecionar o mês/ano atual no combobox	
	var data = new Date();
	var mesAtual = data.getMonth();
	var anoAtual = data.getFullYear();
	$('#lanc_meses').val(mesAtual).prop('selected', true);
	$('#lanc_meses_change').val(mesAtual).prop('selected', true);
	$('#lanc_anos').val(anoAtual).prop('selected', true);
	$('#lanc_anos_change').val(anoAtual).prop('selected', true);

	$('.filtrar').on('click', function() {

		$('#card_atual').hide();
		$('#card_change').show();

		var mes = parseInt($('#lanc_meses_change').val()) + 1;
		var ano = $('#lanc_anos_change').val()

		$.ajax({
			type: 'POST',
			url: '/caixa/',
			data: {
				'mes': mes,
				'ano': ano,
				'csrfmiddlewaretoken': csrftokenPOST
			},
			datatype: 'json',
			success: function(lancamentos) {
				var table = $('#dataCaixaChange').DataTable();

				var rows = table.clear().draw();					

				if(lancamentos.length !== 0) {

					for(var x = 0; x < lancamentos.length; x++) {

						data = lancamentos[x].fields.data;
						dia = data.substring(8);
						mes = data.substring(5, 7);
						ano = data.substring(0, 4);
						newData = dia + "/" + mes + "/" + ano;

						if(lancamentos[x].fields.categoria[1] === "1") {
							var categoria = "<span style='color: blue' >" + lancamentos[x].fields.valor + "</span>";
						}else{
							var categoria = "<span style='color: red' >" + lancamentos[x].fields.valor + "</span>";
						}

						table.row.add([newData,
						lancamentos[x].fields.descricao,
						lancamentos[x].fields.categoria[2],
						categoria,
						"<i class='material-icons'><a data-toggle='modal' href=''><span class='openEdit' data-lanc=" + lancamentos[x].pk + ">edit</span></a></i>"
						]).draw(false);
					}
				}					
			},
			error: function(msg) {
				//mensagem de retorno em caso de erro
				$.alert('erro')
				console.log(msg.responseText);
				
			},
		});
	});

	//Deixar os valores das duas caixa iguais
	$('#lanc_anos').on('change', function() {
		$('#lanc_anos_change').val($('#lanc_anos').val()).prop('selected', true);
	})

	$('#lanc_meses').on('change', function() {
		$('#lanc_meses_change').val($('#lanc_meses').val()).prop('selected', true);
	})

});
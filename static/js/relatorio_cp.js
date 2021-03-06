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

	$('#card_result').hide();

	$('#form_relatorio_cp').on('submit', function(evento) {
		evento.preventDefault();

		var inicio = $('#vencimento_inicial').val();
		var fim = $('#vencimento_final').val();
		var status = $('#status_pagamento').val();

		if(status === 'nenhum') {
			$.alert("Escolha o status da conta.");
		}
		else {
			var dataInicio = new Date(converteData(inicio));
			var dataFim = new Date(converteData(fim));
			
			if(dataInicio > dataFim) {
				$.alert("Período inválido. Data inicial maior que a data final.");
			}
			else {
				$.ajax({
					type: 'POST',
					url: '/relatorios/contas_a_pagar/',
					data: {
						'inicio': inicio,
						'fim': fim,
						'status': status,
						'csrfmiddlewaretoken': csrftokenPOST,
					},
					success: function(contas) {
						
						var table = $('#dataRelatorioCP').DataTable();
						var rows = table.clear().draw();
						var total = 0.0;

						if(contas.length !== 0) {					

							for(var x = 0; x < contas.length; x++) {
								total += parseFloat(contas[x].fields.valor);
								var valor = contas[x].fields.valor;
								

								data = contas[x].fields.data;
								dia = data.substring(8);
								mes = data.substring(5, 7);
								ano = data.substring(0, 4);
								newData = dia + "/" + mes + "/" + ano;

								table.row.add([newData,
								contas[x].fields.descricao,
								contas[x].fields.categoria[2],
								valor.replace('.', ','),
								]).draw(false);
							}

							//preenchimento das tags de acordo do o filtro
							$('#totalCP').html(String(total.toFixed(2)).replace('.', ','));
							$('#inicial_cp').html(inicio);
							$('#final_cp').html(fim);

						}
						else {
							$('#totalCP').html("0,0");
							$('#inicial_cp').html(inicio);
							$('#final_cp').html(fim);
						}

						//oculta/exibe os cards
						$('#card_filter').hide();
						$('#card_result').show();


						if(status === "vencidas") {
							$('#statusCP').html("Vencidas")
						}
						else if(status === "pagas") {
							$('#statusCP').html("Pagas")
						}
						else if(status === "a_pagar") {
							$('#statusCP').html("A Pagar")
						}
					},
					error: function(msg) {

					},
				});
			}

			
		}
		
	});

	function converteData(data) {
		dia = data.substring(0, 2);
		mes = data.substring(3, 5);
		ano = data.substring(6)

		var newData = ano + "-" + mes + "-" + dia

		return newData
	}

	$('.voltar').on('click', function() {
		$('#card_filter').show();
		$('#card_result').hide();
	});
});
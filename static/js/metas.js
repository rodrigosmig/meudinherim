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

	$('#form_cadastro_meta').on('submit', function(evento) {
		
		evento.preventDefault();
		
		var inicio = $('#datepickerMI').val();
		var fim = $('#datepickerMF').val();
		var titulo = $('#id_titulo').val();
		var valor = $('#id_valor_meta').val();

		$.ajax({
			type: 'POST',
			url: '/metas/',
			data: {
				'dataInicio': inicio,
				'dataFim': fim,
				'titulo': titulo,
				'valor': valor,
				'csrfmiddlewaretoken': csrftokenPOST,	
			},
			success: function(msg) {
				//mensagem de confirmação
				$.alert({
					title: false,
					content: msg,
					theme: 'material',
					onClose: function() {
						//limpar campos
						$(".modal-body input").val("");
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

	$('#form_edit_cadastro').on('submit', function(evento) {
		
		evento.preventDefault();
		
		var dados = recuperCampos();

		$.ajax({
			type: 'POST',
			url: '/metas/edit/',
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
		var dados = recuperCampos();

		$.confirm({
		    title: 'Excluir meta!',
		    content: 'Tem certeza que deseja excluir a meta?',
		    draggable: true,
		    theme: 'material',
		    buttons: {
		        Sim: function() {
		        	$.ajax({
		        		type: 'POST',
						url: '/metas/delete/',
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
		        	})
		        },
		        Não: function() {},
		    }
		});
	});

	$(document).on('click', '.conclui_meta', function() {
		var id_meta = $(this).attr('data-meta')
		var concluida = $(this).attr('data-concluida')
		console.log(concluida)
		var html = "<div class='preloader pl-size-xs'> \
					<div class='spinner-layer pl-red-grey'> \
					<div class='circle-clipper left'> \
					<div class='circle'></div> \
					</div> \
					</div> \
					</div>"

		$(this).html(html)

		$.ajax({
			type: 'POST',
			url: '/metas/conclui_meta/',
			dataType: 'JSON',
			data: {
				'id_meta': id_meta,
				'csrfmiddlewaretoken': csrftokenPOST,
			},
			success: function(response) {
				console.log(response)
				insereConcluido(response)
			},
			error: function(msg) {
				if(concluida == "True") {					
					concluida = true
				}
				else {					
					concluida = false	
				}
					
				var response = {
					'concluida': concluida,
					'id': id_meta
				}
				insereConcluido(response)
				$.alert({
					title: false,
					content: "Meta não encontrada",
					theme: 'material',
					/* onClose: function() {
						//recarrega a página
						location.reload();
					} */
				});		
			},
		})
	})

	function insereConcluido(response) {
		if(response.concluida) {
			console.log(response.concluida)
			var html = "<i class='material-icons'><a href='javascript:void(0);' style='color: green' title='Meta concluída. Clique para desfazer.'><span class='conclui_meta' data-meta=" + response.id + " data-concluida=True>done</span></a></i>"
			$("#"+response.id + " .concluida").html(html)
		}
		else {
			console.log("else")
			var html = "<i class='material-icons'><a href='javascript:void(0);' style='color: red' title='Clique para concluir a meta.'><span class='conclui_meta' data-meta=" + response.id + " data-concluida=False>close</span></a></i>"
			$("#"+response.id + " .concluida").html(html)
		}
	}
});
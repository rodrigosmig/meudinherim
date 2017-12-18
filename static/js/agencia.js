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

		var idAgencia = $(this).attr('data-ag');

		$.ajax({
			type: 'GET',
			url: '/banco/editag/',
			data: {'idAgencia': idAgencia, 'csrfmiddlewaretoken': csrftokenGET},
			success: function(lancamento){

				$('#editAgencia').html(lancamento);

				// id quem vem da view id_agencia-alter_agencia
				var id_agencia = $("#temp").html();

				$('#id_banco-alter_banco').attr('data-ag', id_agencia);
				$('#temp').remove();

				console.log('id_agencia')
			},
			error: function(erro) {
				console.log(erro.responseText);
				alert("Lançamento não encontrado. Tente novamente.");
			},

		});
	});


	$('.salvarAg').click(function(evento) {

		evento.preventDefault();

		var campos = recuperaCampos();

			$.ajax({
				type: 'POST',
				url: '/banco/editag/',
				data: campos,
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


	$('.excluirAg').click(function(evento) {
		evento.preventDefault();
		var campos = recuperaCampos();

		$.confirm({
		    title: 'Excluir agência!',
		    content: 'Tem certeza que deseja excluir a agência?',
		    draggable: true,
		    theme: 'material',
		    buttons: {
		        Sim: function() {
		        	$.ajax({
		        		type: 'POST',
						url: '/banco/delag/',
						data: campos,
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


	function recuperaCampos() {

		var id = $('#id_banco-alter_banco').attr('data-ag');
		var banco = $('#id_banco-alter_banco').val();
		var agencia = $('#id_agencia-alter_agencia').val();
		var conta = $('#id_conta-alter_conta').val();
		var tipo = $('#id_tipo-alter_tipo').val();

		console.log(id);

		dados = {
			'id': id,
			'banco': banco,
			'agencia': agencia,
			'conta': conta,
			'tipo': tipo,
			'csrfmiddlewaretoken': csrftokenPOST
		}
		console.log(dados);
		return dados;
	}

})
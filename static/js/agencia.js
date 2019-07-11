$(function() {
	var spinner =  "<div class='preloader pl-size-xs' style: font-size 5px> \
                  <div class='spinner-layer'> \
                  <div class='circle-clipper left'> \
                  <div class='circle'></div> \
                  </div> \
                  <div class='circle-clipper right'> \
                  <div class='circle'></div> \
                  </div> \
                  </div> \
                  </div>";	

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

			},
			error: function(erro) {
				$("#editAg").modal('hide')
				alert("Lançamento não encontrado. Tente novamente.");
			},

		});
	});

	/* $('#form_cadastro_agencia').on('submit', function(evento) {
		evento.preventDefault();

		var banco = $('#id_banco_agencia').val();
		var agencia = $('#id_agencia').val();
		var conta = $('#id_conta').val();
		var tipo = $('#id_tipo_agencia').val()

		$.ajax({
			type: 'POST',
			url: '/banco/agencia/',
			data: {
				'banco': banco,
				'agencia': agencia,
				'conta': conta,
				'tipo': tipo,
				'csrfmiddlewaretoken': csrftokenPOST
			},
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
	}); */


	$('.salvarAg').on('click', function(evento) {
		var id = $('#id_banco-alter_banco').attr('data-ag');
		
		if(id) {
			$("#form_edit_agencia").append("<input type='hidden' name='id_agencia' value=" + id + " />")
			$("#form_edit_agencia").append("<input type='hidden' name='alterar' value='alterar' />")
			$(".salvarAg").attr('disabled', 'true')
			$(".excluirAg").attr('disabled', 'true')
			$(".cancelarAg").attr('disabled', 'true')
			$(".loading").append(spinner)
			$('#form_edit_agencia').attr('action', '/banco/editag/')

			$('#form_edit_agencia').submit()
		}		
		
	});


	$('.excluirAg').click(function(evento) {
		evento.preventDefault();
		var id = $('#id_banco-alter_banco').attr('data-ag');

		$.confirm({
		    title: 'Excluir Conta!',
		    content: 'Tem certeza que deseja excluir a conta ?',
		    draggable: true,
		    theme: 'material',
		    buttons: {
		        Sim: function() {
		        	$("#form_edit_agencia").append("<input type='hidden' name='id_agencia' value=" + id + " />")
					$(".salvarAg").attr('disabled', 'true')
					$(".excluirAg").attr('disabled', 'true')
					$(".cancelarAg").attr('disabled', 'true')
					$(".loading").append(spinner)
					$('#form_edit_agencia').attr('action', '/banco/delag/')

					$('#form_edit_agencia').submit()
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
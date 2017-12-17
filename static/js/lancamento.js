$(function() {
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

	$('.salvarCaixa').on('click', function(event) {
		var data = $('#datepickerC').val();
		var categoria = $('#id_categoria').val();
		var descricao = $('#id_descricao').val();
		var valor = $('#id_valor').val();

		var dados = {
			'data': data,
			'categoria': categoria,
			'descricao': descricao,
			'valor': valor,
			'csrfmiddlewaretoken': csrftokenPOST
		}

		$.ajax({
			type: 'POST',
			url: '/caixa/add/',
			data: dados,
			success: function(msg) {
				//mensagem de confirmação
				alert(msg);
				//limpar campos
				$(".modal-body input").val("");
				//recarregar pagina
				location.reload();
			},
			error: function(msg) {
				alert(msg);
			},
		});
	});

	$('.salvarBanco').on('click', function(event) {
		var banco = $('#id_banco').val();
		var data = $('#datepickerB').val();
		var tipo = $('#id_tipo').val();
		var categoria = $('#categoria_banco').val();
		var descricao = $('#desc_Banco').val();
		var valor = $('#valor_banco').val();

		var dados = {
			'banco': banco,
			'data': data,
			'tipo': tipo,
			'categoria': categoria,
			'descricao': descricao,
			'valor': valor,
			'csrfmiddlewaretoken': csrftokenPOST
		}

		$.ajax({
			type: 'POST',
			url: '/banco/add/',
			data: dados,
			success: function(msg) {
				//mensagem de confirmação
				alert(msg);
				//limpar campos
				$(".modal-body input").val("");
				//recarregar pagina
				location.reload();
			},
			error: function(msg) {
				alert(msg);
			},
		});
	});
})
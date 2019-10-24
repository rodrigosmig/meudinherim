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
		//atribui o id da categoria a variavel
		var id = $(this).attr('data-cat');
		//envia a solicitacao do formulario com o id da categoria via ajax
		$.ajax({
			type: 'GET',
			url: '/caixa/edit-categoria/',
			data: {'id': id, 'csrfmiddlewaretoken': csrftokenGET},
			success: function(categoria) {
				//insere o form vindo do django na div editCate
				$('#editCate').html(categoria);

				//Atribui o id da categoria a uma tag e remove a div vinda do Django
				var id_categoria = $('#id-alter_categoria').html();
				$('#id_categoria-alter_categoria').val(id_categoria);
				$('#id-alter_categoria').remove();
				
			},
			error: function(erro) {
				console.log(erro.responseText);
				alert("Categoria não encontrada. Tente novamente.");
			},

		});
	});

	$('.excluir').click(function(evento) {
		evento.preventDefault();
		var id = $('#id_categoria-alter_categoria').val();

		$.confirm({
		    title: 'Excluir categoria!',
		    content: 'Tem certeza que deseja excluir a categoria?',
		    draggable: true,
		    theme: 'material',
		    buttons: {
		        Sim: function() {
					$('#form_edit_categoria').attr('action', '/caixa/delete-categoria/')
					$('#form_edit_categoria').submit()
		        },
		        Não: function() {
					return
				},
		    }
		});
	});
})
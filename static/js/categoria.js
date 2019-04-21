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
				$('#id_descricao-alter_categoria').attr('data-cat', id_categoria);
				$('#id-alter_categoria').remove();
				
			},
			error: function(erro) {
				console.log(erro.responseText);
				alert("Categoria não encontrada. Tente novamente.");
			},

		});
	});

	$('#form_cadastro_categoria').on('submit', function(event) {
		$(".cadastrar_categoria").attr('disabled', 'true')
		$(".cancelar_categoria").attr('disabled', 'true')
		$(".loading").append(spinner)
	});

	$('.editar_categora').on('click', function(event) {
		var id = $('#id_descricao-alter_categoria').attr('data-cat');
		if(id) {
			$("#form_edit_categoria").append("<input type='hidden' name='id_categoria' value=" + id + " />")
			$("#form_edit_categoria").append("<input type='hidden' name='alterar' value='alterar' />")
			$(".editar_categora").attr('disabled', 'true')
			$(".excluir").attr('disabled', 'true')
			$(".cancelar_categoria").attr('disabled', 'true')
			$(".loading").append(spinner)
			$("#form_edit_categoria").submit()
		}
		
	});

	$('.excluir').click(function(evento) {
		evento.preventDefault();
		var id = $('#id_descricao-alter_categoria').attr('data-cat');

		$.confirm({
		    title: 'Excluir meta!',
		    content: 'Tem certeza que deseja excluir a categoria?',
		    draggable: true,
		    theme: 'material',
		    buttons: {
		        Sim: function() {
					if(id) {
						$("#form_edit_categoria").append("<input type='hidden' name='id_categoria' value=" + id + " />")
						$("#form_edit_categoria").append("<input type='hidden' name='excluir' value='excluir' />")
						$(".editar_categora").attr('disabled', 'true')
						$(".excluir").attr('disabled', 'true')
						$(".cancelar_categoria").attr('disabled', 'true')
						$(".loading").append(spinner)
						$("#form_edit_categoria").submit()
					}					
		        },
		        Não: function() {
					return
				},
		    }
		});
	});
})
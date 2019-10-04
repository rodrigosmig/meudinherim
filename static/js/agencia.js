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
			success: function(agencia){

				$('#editAgencia').html(agencia);

				// id quem vem da view id_agencia-alter_agencia
				var id_agencia = $("#temp").html();

				$('#id_banco-id_alter_banco').val(id_agencia);
				$('#temp').remove();

				$("#id_conta-alter_dia_fechamento").datepicker({
					changeMonth: false,
					changeYear: false,
					dateFormat: 'dd',
					dayNames: ['Domingo','Segunda','Terça','Quarta','Quinta','Sexta','Sábado'],
					dayNamesMin: ['D','S','T','Q','Q','S','S','D'],
					dayNamesShort: ['Dom','Seg','Ter','Qua','Qui','Sex','Sáb','Dom'],
					monthNames: ['Janeiro','Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro','Novembro','Dezembro'],
					monthNamesShort: ['Jan','Fev','Mar','Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez'],
					nextText: 'Próximo',
					prevText: 'Anterior'
				}).focus(function() {
					$(".ui-datepicker-prev, .ui-datepicker-next, .ui-datepicker-month, .ui-datepicker-year").remove();
				})

			},
			error: function(erro) {
				$("#editAg").modal('hide')
				alert("Lançamento não encontrado. Tente novamente.");
			},

		});
	});

	$('.excluirAg').click(function(evento) {
		evento.preventDefault();
		var id = $('#id_banco-id_alter_banco').val();

		$.confirm({
		    title: 'Excluir Conta!',
		    content: 'Tem certeza que deseja excluir a conta ?',
		    draggable: true,
		    theme: 'material',
		    buttons: {
		        Sim: function() {
					$('#form_edit_agencia').attr('action', '/banco/delag/')
					$('#form_edit_agencia').submit()
		        },
		        Não: function() {},
		    }
		});
	});



})
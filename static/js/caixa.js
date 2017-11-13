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
			data: {'id': id, 'csrfmiddlewaretoken': csrftokenGET},
			success: function(lancamento) {
				//insere o form vindo do django na div editLanc
				$('#editLanc').html(lancamento);

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

	$('.salvar').click(function(evento) {
		evento.preventDefault();
		
		var dados = recuperCampos();
		console.log(dados);

		$.ajax({
			type: 'POST',
			url: '/caixa/edit/',
			data: dados,
			success: function(msg) {
				//mensagem de confirmação
				alert(msg);
				//recarregar pagina
				location.reload();
			},
			error: function(msg) {
				alert(msg);
			},
		});		
	});

	$('.excluir').click(function(evento) {
		evento.preventDefault();

		if(confirm("Tem certeza que deseja excluir o lançamento?")) {
			var dados = recuperCampos();
			$.ajax({
				type: 'POST',
				url: 'delete/',
				data: dados,
				success: function(msg) {
					//mensagem de confirmação
					alert(msg);
					//recarregar pagina
					location.reload();
				},
				error: function(msg) {
					//mensagem de retorno em caso de erro
					alert(msg)
				},
			});
		}
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

	$('#card_change').hide();

	//gerar combobox com os meses anteriores
	var meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'];
	var data = new Date();
	var mesAtual = data.getMonth();
	var conteudo = "";
	
	
	for(var x = 0; x <= mesAtual; x++) {
		if(x === mesAtual) {
			conteudo += "<option value =" + (x + 1) + " selected>" + meses[x] + "</option>";
		}
		else {
			conteudo += "<option value =" + (x + 1) + ">" + meses[x] + "</option>";
		}
	}
	$('#lanc_meses').html(conteudo);

	$('#lanc_meses').on('change', function() {
		
		$('#card_atual').hide();
		$('#card_change').show();

		var mes = $(this).val();

		$.ajax({
			type: 'POST',
			url: '/caixa/',
			data: {'mes': mes, 'csrfmiddlewaretoken': csrftokenPOST},
			datatype: 'json',
			success: function(lancamentos) {
				var table = $('#dataCaixaChange').DataTable();

				var rows = table.clear().draw();					

				if(lancamentos.length !== 0) {

					for(var x = 0; x < lancamentos.length; x++) {

						data = lancamentos[x].fields.data;
						dia = data.substring(8);
						mes = data.substring(5, 7);
						ano = data.substring(0, 4)
						newData = dia + "/" + mes + "/" + ano

						table.row.add([newData,
						lancamentos[x].fields.descricao,
						lancamentos[x].fields.categoria[1],
						lancamentos[x].fields.valor,
						"teste",
						"<i class='material-icons'><a data-toggle='modal' href=''><span class='openEdit' data-lanc=" + lancamentos[x].pk + ">edit</span></a></i>"
						]).draw(false);

					}
				}					
			},
			error: function(msg) {
				//mensagem de retorno em caso de erro
				alert('erro')
				console.log(msg)
				
			},
		});
	})

});
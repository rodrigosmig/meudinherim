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
    
    function convertDate(date) {
        var dia = date.substring(8)
        var mes = date.substring(5, 7)
        var ano = date.substring(0, 4)
        var newDate = dia + "/" + mes + "/" + ano
        return newDate
    }

	$(document).on('click', '.openDetails', function() {
        var categoria_id    = $(this).attr('data-categoria');
        var tipo_conta      = $(this).attr('data-tipo');

		$.ajax({
			type: 'GET',
			url: '/principal/detalhes/',
            data: {
                'categoria_id': categoria_id,
                'tipo_conta': tipo_conta,
                'csrfmiddlewaretoken': csrftokenGET
            },
			success: function(lancamentos){
                $('#labelCategoria').html(lancamentos[0].fields.categoria[2])
                for (var index = 0; index < lancamentos.length; index++) {
                    var data = convertDate(lancamentos[index].fields.data)
                    var valor =lancamentos[index].fields.valor.replace('.', ',')

                    html = "<tr> \
                        <td> " + (index + 1) + "</td> \
                        <td> " + lancamentos[index].fields.descricao + "</td> \
                        <td> " + data + "</td> \
                        <td> " + valor + "</td> \
                    </tr>"
                    $("#table-body").append(html)                    
                }
			},
			error: function(erro) {
				$("#modalDetalhes").modal('hide')
				$.alert("Categoria não encontrada. Tente novamente.");
			},

		});
    });
    
    $('#modalDetalhes').on('hidden.bs.modal', function (e) {
        $('#table-body').html("")
    })
    
    $('#mes_anterior').on('click', function(evento) {
        evento.preventDefault();
        var tipo = $(this).attr('data-mes')
        console.log(tipo)
        $("#form_mes").append("<input type='hidden' name='mes' value=" + tipo + " />")
        $("#mes_anterior").attr('disabled', true)
        $("#mes_seguinte").attr('disabled', true)
        $("#form_mes").submit()
    })

    $('#mes_seguinte').on('click', function(evento) {
        evento.preventDefault();
        var tipo = $(this).attr('data-mes')
        $("#form_mes").append("<input type='hidden' name='mes' value=" + tipo + " />")
        $("#mes_anterior").attr('disabled', true)
        $("#mes_seguinte").attr('disabled', true)
        $("#form_mes").submit()
    })

   
})
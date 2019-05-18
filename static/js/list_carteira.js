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
    
    $.ajax({
        type: 'GET',
			url: '/caixa/saldo/',
			data: {
				'csrfmiddlewaretoken': csrftokenGET
            },
            success: function(saldoCaixa) {
                saldoCaixa.forEach(saldo => {
                    var html = "<li> \
                                <a class='waves-effect waves-block teste' href='javascript:void(0);'> \
                                <span class='i-circle'>$</span> \
                                <div class='menu-info'> \
                                <h4>Saldo: " + saldo.fields.saldoAtual + "</h4> \
                                </div> \
                                </a> \
                                </li>"

                    $('#menudfdf_carteira').append(html)
                    $("#total_carteira").html(" " + saldo.fields.saldoAtual.replace(".", ","))
                });
           
                $('#quantidade_carteira').html(saldoCaixa.length);
                
            },
            error: function(erro) {
                var html = "<li style='text-align: center'> \
                            <a class='waves-effect waves-block' href='javascript:void(0);'>Sem metas para exibir</a> \
                            </li>"

                $('#menu_metas').append(html)
                $('#quantidade_metas').html(0)
			},
    })
})
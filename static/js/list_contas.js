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
			url: '/banco/getAgencias/',
			data: {
				'csrfmiddlewaretoken': csrftokenGET
            },
            success: function(agencias) {
                if(agencias.length == 0) {
                    var html = "<li style='text-align: center'> \
                            <a class='waves-effect waves-block' href='javascript:void(0);'>Sem agências para exibir</a> \
                            </li>"

                    $('#menu_contas').append(html)
                }
                else {
                    var soma = 0;
                    agencias.forEach(agencia => {
                        soma += parseFloat(agencia.fields.saldo)
                        var html = "<li> \
                                    <a class='waves-effect waves-block teste' href='javascript:void(0);'> \
                                    <span class='i-circle'>" + agencia.fields.banco.substring(0, 1).toUpperCase() + "</span> \
                                    <div class='menu-info'> \
                                    <h4>" + agencia.fields.banco + "</h4> \
                                    <p> \
                                    <i class='material-icons'>attach_money</i>Saldo: <b>R$ " + agencia.fields.saldo.replace(".", ",") + "</b> \
                                    </p> \
                                    </div> \
                                    </a> \
                                    </li>"
    
                        $('#menu_contas').append(html)
                    });
                }                
                $('#quantidade_contas').html(agencias.length);
                if(soma >= 0) {
                    $("#total_contas").html("R$ " + soma.toFixed(2).replace(".", ",")).css('color', 'blue');
                }
                else {
                    $("#total_contas").html("R$ " + soma.toFixed(2).replace(".", ",")).css('color', 'red');
                }
                
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
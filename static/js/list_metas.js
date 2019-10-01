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
			url: '/metas/calc_metas/',
			data: {
				'csrfmiddlewaretoken': csrftokenGET
            },
            success: function(metas) {
                if(metas.length == 0) {
                    var html = "<li style='text-align: center'> \
                            <a class='waves-effect waves-block' href='javascript:void(0);'>Sem metas para exibir</a> \
                            </li>"

                    $('#menu_metas').append(html)
                }
                else {
                    metas.forEach(meta => {
                        if(meta.fields.progresso < 30 ) {
                            cor_progresso = "progress-bar-danger"
                        }
                        else if(meta.fields.progresso < 80) {
                            cor_progresso = "bg-cyan"
                        }
                        else {
                            cor_progresso = "progress-bar-success"
                        }
                        var html = "<li> \
                               <a class='waves-effect waves-block' href='javascript:void(0);'> \
                               <h4> \
                               " + meta.fields.titulo + " - R$" + meta.fields.valor + " \
                               <small>" + meta.fields.progresso + "%</small> \
                               </h4> \
                               <div class='progress'> \
                               <div class='progress-bar " + cor_progresso + " role='progressbar' aria-valuenow='85' aria-valuemin='0' aria-valuemax='100' style='width:" + meta.fields.progresso + "%'> \
                               </div> \
                               </div> \
                               </a> \
                               </li>"
    
                        $('#menu_metas').append(html)
                    });
                }                
                $('#quantidade_metas').html(metas.length)
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
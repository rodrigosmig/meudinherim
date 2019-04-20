$(function() {
  var spinner =  "<div class='preloader pl-size-xs'> \
                  <div class='spinner-layer'> \
                  <div class='circle-clipper left'> \
                  <div class='circle'></div> \
                  </div> \
                  <div class='circle-clipper right'> \
                  <div class='circle'></div> \
                  </div> \
                  </div> \
                  </div>"

  $('input[type=file]').change(function(event) {
    var t = $(this).val();
    var labelText = 'Imagem: ' + t.substr(12, t.length);    
    $(this).prev('label').text(labelText);

    var imagem = URL.createObjectURL(event.target.files[0])
    $('.image-area').html("<img src=" + imagem +" width='130' height='130' >")

    $('#submit_foto').removeAttr('disabled')
  })

  $('#form_perfil').on('submit', function() {
    $('#submit_perfil').html(spinner)
  })

  $('#form_senha').on('submit', function() {
    $('#submit_senha').html(spinner)      
  })

  $('#submit_foto').on('click', function() {
    if($('#id_foto').val() == "") {
      $.alert({
        title: false,
        content: "Selecione uma imagem",
        theme: 'material',
      });
      return
    }
    $(this).attr('disabled', 'true')
    $(this).html(spinner)
    $('#formImg').submit()
  })
});
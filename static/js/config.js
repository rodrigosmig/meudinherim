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
  $('#salvar_foto').attr('disabled', true)

  $('input[type=file]').change(function() {
    var t = $(this).val();
    var labelText = 'Imagem: ' + t.substr(12, t.length);
    $(this).prev('label').text(labelText);

    $('#salvar_foto').removeAttr('disabled')
  })

  $('#form_perfil').on('submit', function() {
    $('#submit_perfil').html(spinner)
  })

  $('#form_senha').on('submit', function() {
    $('#submit_senha').html(spinner)      
  })
});
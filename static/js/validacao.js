$(function() {
	$('#sign_up').on('submit', function(evento) {

		if ($('#id_password1').val().length < 6 || $('#id_password2').val().length < 6) {
			$.alert("A senha deve ter no mínimo 6 caracteres");
			return false;
		}
		else if ($('#id_password1').val() != $('#id_password2').val()) {
			$.alert("Ops, senhas não conferem!");
			return false;
		}
	});
});
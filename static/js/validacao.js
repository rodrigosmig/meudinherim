
function validarLogin(){

	if (formLogin.login.value == "") {

		alert("Por favor, preencha o campo usuário.");
		formLogin.login.focus();
		return false;
	}

	if (formLogin.senha.value.length < 6 ) {

		alert("A senha deve ter no mínimo 6 caracteres");
		formLogin.senha.focus();
		return false;
	}

}

function validarCadastro(){

	if (formCadastro.username.value == "") {

		alert("Por favor, preencha o campo usuário.");
		formCadastro.username.focus();
		return false;
	}

	if(formCadastro.email.value == "" ||
		formCadastro.email.value.indexOf('@') == -1 ||
		formCadastro.email.value.indexOf('.') == -1 ){

		alert("Por favor, digite um endereço de e-mail válido!");
		formCadastro.email.focus();
		return false;
	}

	if (formCadastro.password1.value.length < 6) {

		alert("A senha deve ter no mínimo 6 caracteres");
		formCadastro.password1.focus();
		return false;
	}

	if (formCadastro.password2.value.length < 6) {

		alert("A senha deve ter no mínimo 6 caracteres");
		formCadastro.password1.focus();
		return false;
	}

	if (formCadastro.password1.value != formCadastro.password2.value) {

		alert("Ops, senhas não conferem!");
		formCadastro.password2.focus();
		return false;
	}
}
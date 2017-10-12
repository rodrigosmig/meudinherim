

function validarCadastro(){
    var senha=formCadastrar.tSenha.value;
    var rep_senha=formCadastrar.tConfSenha.value;
    var nomePessoa=formCadastrar.tNome.value;
    var emailPessoa=formCadastrar.tMail.value;
    
    if(nomePessoa==""){
        alert('Preencha o campo NOME !')
        formCadastrar.tNome.focus();
        return false;
    }
    
    if(emailPessoa==""){
        alert('Preencha o campo E-MAIL !')
        formCadastar.tMail.focus();
        return false;
    }
    
    if(senha == "" || senha.length<=5){
        alert('Preencha o campo com mínimo 6 caracteres')
        formCadastrar.tSenha.focus();
        return false;
    }
    
    
    
      if(senha != rep_senha){
        alert('Senhas diferntes')
        formCadastrar.tConfSenha.focus();
        return false;
    }
  
}



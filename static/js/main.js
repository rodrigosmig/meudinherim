

function validar(){
    var senha=formCadastrar.tSenha.value;
    var rep_senha=formCadastrar.tConfSenha.value;
    
        
    if(senha == "" || senha.length<=5){
        alert('Preencha o campo com mínimo 6 caracteres')
        formCadastrar.tSenha.focus();
        return false;
    }
    
     if(rep_senha == "" || rep_senha.length<=5){
        alert('Preencha o campo com mínimo 6 caracteres')
        formCadastrar.tConfSenha.focus();
        return false;
    }
    
      if(senha != rep_senha){
        alert('Senhas diferntes')
        formCadastrar.tConfSenha.focus();
        return false;
    }
    
}
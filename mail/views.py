import os
from django.shortcuts import render, redirect
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime
from django.http import HttpResponse
from usuario.models import UsuarioProfile
from contas_a_pagar.models import ContasAPagar
from django.template.loader import render_to_string
from django.template.loader import get_template

def CronContasAPagar(request):
    users = UsuarioProfile.objects.filter(mail_contas_a_pagar = True)
    today = datetime.today().strftime("%Y-%m-%d")
    
    for user in users:
        accounts = ContasAPagar.objects.filter(user = user.user).filter(data = today).filter(paga = False)
        html = render_to_string('mail/contas_a_pagar.html', {'contas': accounts, 'data': datetime.today()})
    
        message = Mail(
            from_email='contas_a_pagar@meudinherim.ovh',
            to_emails=user.user.email,
            subject="Contas com vencimento dia " + datetime.today().strftime("%d/%m/%Y"),
            html_content=html)

        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)

    
    #return render(request, 'mail/contas_a_pagar.html')
    return HttpResponse("Deu certo")
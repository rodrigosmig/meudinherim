import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.http import HttpResponse

def CronContasAPagar(request):
    message = Mail(
        from_email='contas_a_pagar@meudinherim.ovh',
        to_emails='rodrigosmig@outlook.com',
        subject='Email de teste',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

    return HttpResponse("Deu certo")
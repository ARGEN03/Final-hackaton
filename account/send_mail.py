from django.core.mail import send_mail

def send_confirmation_email(email, code):
    activation_url = f'http://localhost:8000/account/activate/?u={code}'
    subject = 'Активация аккаунта'
    message = f'Для активации аккаунта перейдите по ссылке: {activation_url}'
    from_email = 'fitstreety@gmail.com'
    recipient_list = [email]

    send_mail(
        subject, 
        message, 
        from_email, 
        recipient_list
    )
   
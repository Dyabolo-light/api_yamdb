from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response

from .models import ConfirmationCode


def get_confirmation_code(data):
    email = data.get('email')
    username = data.get('username')
    code = ConfirmationCode.objects.create(
        confirmation_code='12345'
        # confirmation_code=uuid.uuid4().hex[:4].upper()
    )
    send_mail(
        "Confirmation",
        f"Your confirmation code {code}",
        "from@example.com",
        [email],
        fail_silently=False,
    )
    return {'username': str(username), 'email': str(email)}

import random
import string
from celery import shared_task
from django.core.mail import send_mail
from .models import User

# just for testing chnage_name def
def generate_random_string(length):
    letters = string.ascii_letters  # شامل حروف کوچک و بزرگ
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

@shared_task
def send_verification_email(user_email):
    send_mail(
        'Verify your email',
        'Please verify your email by clicking the link below.',
        'from@example.com',
        [user_email],
        fail_silently=False,
    )

# just for test
@shared_task
def change_name(user_email):
    user = User.objects.get(email=user_email)
    user.username = generate_random_string(8)
    user.save()
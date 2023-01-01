from django.conf import settings
from twilio.rest import Client
import random

class MessageHandler:
    phone_number = None
    otp = None

    def __init__(self, phone_number, otp):
        self.phone_number = phone_number
        self.otp = otp

    def send_otp(self):
        client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

        message = client.messages \
                        .create(
                            body=f"Your otp is {self.otp}",
                            from_='+15017122661',
                            to='+15558675310'
                        )

        print(message.sid)
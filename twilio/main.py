from decouple import config
from twilio.rest import Client

def sendTextMessage(message):
    client = Client(config('TWILIO_ACCOUNT_SID'), config('TWILIO_AUTH_TOKEN'))

    client.messages.create(
        to=config('PERSONAL_PHONE_NUMBER'),
        from_=config('TWILIO_PHONE_NUMBER'),
        body=message
    )

if __name__ == '__main__':
    sendTextMessage('Hello from Python!')
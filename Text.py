# import smtplib
# from email.message import EmailMessage

# def text(subject, body, to):
#     msg = EmailMessage()
#     msg.set_content(body)
#     msg['subject'] = subject
#     msg['to'] = to
    
#     user = "trentonblackthorn@gmail.com"
#     msg['from'] = user
#     password = "Dawkinator73"

#     server = smtplib.SMTP("smtp.gmail.com", 587)
#     server.starttls()
#     server.login(user, "qeyu imlk cidf sjmd")
#     server.send_message(msg)

#     server.quit()


# if __name__ == '__main__':
#     text("Hey", "Hello world", "7256001255@sms.myboostmobile.com")

#     print("Yo")



# from twilio.rest import Client
# import keys

# print(keys.account_sid)
# print(keys.auth_token)

# client = Client(keys.account_sid, keys.auth_token)

# message = client.messages.create(
#     body = "This is a new message from Code Palace!",
#     from_=keys.twilio_number,
#     to=keys.my_phone_number
# )


# print(message.body)



# import vonage
# import keys

# client = vonage.Client(key=keys.vonage_key, secret=keys.vonage_secret)
# sms = vonage.Sms(client)


# responseData = sms.send_message(
#     {
#         "from": "12394435296",
#         "to": "17256001255",
#         "text": "A text message sent using the Nexmo SMS API",
#     }
# )

# if responseData["messages"][0]["status"] == "0":
#     print("Message sent successfully.")
# else:
#     print(f"Message failed with error: {responseData['messages'][0]['error-text']}")



import os
from vonage import Vonage, Auth
from vonage_sms import SmsMessage
import keys
import SQLFuntime
import requests

def sendInitialSMS(num: str):
    resp = requests.post('https://textbelt.com/text', {
    'phone': str(num),
    'message': "It’s Sarah from Meridian Health. Is this the same John that got a quote from us in the last couple of months?",
    'key': 'f916ba45a7370060efd35edf8ee15bd4150559c4mO5Qc1cvtI0R6zRDC7nxzr0i7',
    'replyWebhookUrl': 'https://mailing-florida-alice-nitrogen.trycloudflare.com/inbound',
    })

    SQLFuntime.create_number(num, "Sarah: It’s Sarah from Meridian Health. Is this the same John that got a quote from us in the last couple of months?")
    return resp

def sendSMS(num: str, text: str):
    resp = requests.post('https://textbelt.com/text', {
    'phone': str(num),
    'message': text,
    'key': 'f916ba45a7370060efd35edf8ee15bd4150559c4mO5Qc1cvtI0R6zRDC7nxzr0i7',
    'replyWebhookUrl': 'https://short-politicians-arabia-booking.trycloudflare.com/inbound',
    })
    return resp
    

if __name__ == "__main__":
    #sendSMS("+17256001255", "Hello from Vonage + Python")
    


    resp = sendInitialSMS(str(7256001255))
    
    print(resp.json)
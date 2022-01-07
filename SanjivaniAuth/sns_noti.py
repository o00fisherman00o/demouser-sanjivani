from twilio.rest import Client
import random
ph=""


n = random.randint(1000,9999)
def input(pho):
    ph=pho
    account_sid = 'ACf13b83e536e4663c106b477a34fcb5c5'
    auth_token = '934401d3691083688b638aa350c12a57'
    message=f'Sanjivani Organisation Login: \nOTP for your login is {n}'
    client = Client(account_sid, auth_token)

    client.api.account.messages.create(
      to=ph,
      from_="+19387778122",
      body=message)
    return str(n)
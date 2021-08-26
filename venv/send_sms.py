from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "AC8452c9347dfd05685992f192457ee9a9"
# Your Auth Token from twilio.com/console
auth_token  = "22f70069ce42ac448ffd93ad2ca2dca5"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+12534098910",
    from_="+17868286841",
    body="Hello from Python!")

print(message.sid)

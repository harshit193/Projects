import smtplib

sender_email = input('Sender Email: ')
receiver_email = input('Receiver Email: ')

subject = input('Subject: ')
message = input('Message: ')

text = f"Subject: {subject}\n\n{message}"

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()

server.login(sender_email, 'fzfdsixlpxlajbfi')

server.sendemail(sender_email, receiver_email, text)

print(f'email has been sent to {receiver_email}')
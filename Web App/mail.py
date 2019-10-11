import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

pwd='brown_boys1998'



def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(' '.join(a_contact.split()[:-1]))
            emails.append(a_contact.split()[-1])
    return names, emails

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def send_mail(contacts, message, max_aqi, subject='URGENT: Steep incline in Air Pollution predicted. Needs immediate action!!!'):
    s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    s.ehlo()
    s.starttls()
    s.login('brown_boys04@outlook.com', pwd)

    if str(type(contacts)).split()[-1][1:-2]=='str':
        names, emails = get_contacts(contacts)
        message_template = read_template(message)
        for name, email in zip(names, emails):
            msg = MIMEMultipart()  # create a message

            # add in the actual person name to the message template
            message = message_template.substitute(PERSON_NAME=name.title(), XXX=max_aqi)


            # setup the parameters of the message
            msg['From'] = 'brown_boys04@outlook.com'
            msg['To'] = email
            msg['Subject'] = subject

            # add in the message body
            msg.attach(MIMEText(message, 'plain'))

            # send the message via the server set up earlier.
            s.send_message(msg)
            del msg
    else:
        names = [contacts[0]]
        emails = contacts[1]
        message_template = read_template(message)

        for email in emails:
            msg = MIMEMultipart()  # create a message

            message = message_template.substitute(XXX=max_aqi)

            msg['From'] = 'brown_boys04@outlook.com'
            msg['To'] = email
            msg['Subject'] = subject

            # add in the message body
            msg.attach(MIMEText(message, 'plain'))

            # send the message via the server set up earlier.
            s.send_message(msg)
            del msg
    s.quit()




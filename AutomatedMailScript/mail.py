# Import smtplib for the actual sending function
import smtplib

# For guessing MIME type
import mimetypes

# Import the email modules we'll need
import email
import email.mime
import email.mime.text
import email.mime.multipart
from email.mime.multipart import MIMEMultipart
import email.mime.application
FROM='username@gmail.com'
SUBJECT='New Subject'
password='mypassword'
mails = 'mails.txt' #has an e-mail address for each line 
bodyFile='body.txt' # contains e -mail body
transcript='mytranscript.pdf'
cv='myCV.pdf'
attachments=[cv,transcript]


def getMessageBody(textFileName):
    file = open(textFileName,'r')
    body=""
    while True:
        line = file.readline()
        if not line:
            break
        body += line
    return body

def createMessage(FROM,TO,SUBJECT,BODY):
    # Create a text/plain message
    msg = email.mime.multipart.MIMEMultipart()
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = TO

    # The main body is just another attachment
    body = email.mime.text.MIMEText(BODY)
    msg.attach(body)
    return msg

def attachFile(fileName,msg):
    # PDF attachment
    fp=open(fileName,'rb')
    att = email.mime.application.MIMEApplication(fp.read(),_subtype="pdf")
    fp.close()
    att.add_header('Content-Disposition','attachment',filename=fileName)
    msg.attach(att)
    return msg

def connectAndSendMail(msg,password):
    # send via Gmail server
    # NOTE: my ISP, Centurylink, seems to be automatically rewriting
    # port 25 packets to be port 587 and it is trashing port 587 packets.
    # So, I use the default port 25, but I authenticate. 
    try:
        s = smtplib.SMTP('smtp.gmail.com')
        s.starttls()
        s.login(msg['From'],password)
        s.sendmail(msg['From'],msg['To'], msg.as_string())
        s.quit()
        return True
    except:
        return False

def sendToMails(FROM,SUBJECT,textFileName,mailFileName,attachmentList,password):
    BODY=getMessageBody(textFileName)
    file = open(mailFileName,'r')
    s = smtplib.SMTP('smtp.gmail.com')
    s.starttls()
    s.login(FROM,password)

    while True:
        toMail = file.readline()
        if not toMail:
            break
        msg = createMessage(FROM,toMail,SUBJECT,BODY)
        for attachment in attachmentList: 
            msg= attachFile(attachment,msg)
        try:
            s.sendmail(msg['From'],msg['To'], msg.as_string())
        except:
            print("Exception thrown, operation failed.")
            s.quit()
            return False
    s.quit()
    return True

sendToMails(FROM,SUBJECT,bodyFile,mails,attachments,password)

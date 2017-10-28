import logging
import smtplib
from email.mime.text import MIMEText

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


def send_email(subject, content):
    MAIL_LIST = ['cvp@opnfv.org']
    HOST = "smtp.gmail.com"
    USER = "opnfv.cvp"
    PASSWD = "opnfv@cvp"

    sender = 'cvp<{}@gmail.com>'.format(USER)
    msg = MIMEText(content, _subtype='plain')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ";".join(MAIL_LIST)

    _send_email(HOST, sender, USER, PASSWD, MAIL_LIST, msg)


def _send_email(host,
                sender,
                user,
                passwd,
                receivers,
                msg):

    client = smtplib.SMTP()
    try:
        client.connect(host, 25)
        LOG.debug('Success to connect server')
        client.starttls()
        client.login(user, passwd)
        LOG.debug('Success to login')
        LOG.debug('Start to sending email')
        client.sendmail(sender, receivers, msg.as_string())
        client.close()
    except Exception:
        LOG.exception('Error when sending email')
        raise

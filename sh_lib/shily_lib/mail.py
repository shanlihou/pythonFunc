from smtplib import SMTP_SSL 
from email.mime.text import MIMEText 
from email.header import Header
import json
import attr
import functools


HOST = "smtp.qq.com" #不变，QQ邮箱的smtp服务器地址


@attr.s
class Mail(object):
    secret = attr.ib(default='')
    email = attr.ib(default='')

    def send_mail(self, email_to, subject, text):
        smtp = SMTP_SSL(HOST)#SMTP_SSL默认使用465端口
        smtp.login(self.email, self.secret)

        msg = MIMEText(text, "plain", "utf-8")
        msg["Subject"] = Header(subject, "utf-8")
        msg["from"] = self.email
        msg["to"] = email_to

        smtp.sendmail(self.email, email_to, msg.as_string())
        smtp.quit()


@functools.lru_cache(1)
def get_default_user_mail(user_info_path):
    user_info = json.load(open(user_info_path))
    for user in user_info:
        if user['email'].startswith('819'):
            mail = Mail(user['secret'], user['email'])
            return mail


if __name__ == '__main__':
    pass
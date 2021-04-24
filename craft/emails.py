from datetime import date
from django.core.mail import send_mail
from django.conf import settings
from django.apps import apps
import smtplib
from email.mime.text import MIMEText
from email.header import Header


# 调用django自带sendmail未成功，用错误的密码和帐户也会正常返回1.不报错。
def send_foucs_mail():
    '''
    定时发送每日关注给到相关人员的邮箱
    :return:
    '''
    today = date.today().isoformat()

    return send_mail(
        subject=f'今日关注-{today}',
        message='今日关注 邮件尝试',
        from_email='angelyhch@163.com',
        recipient_list=['angelyhch1@163.com'],
        fail_silently=False

    )


def send_mail_self():
    '''
    用smtplib模块重写邮件功能
    :return:
    '''
    mail_host = apps.get_app_config('craft').EMAIL_HOST
    mail_port = apps.get_app_config('craft').EMAIL_PORT
    mail_user = apps.get_app_config('craft').EMAIL_HOST_USER
    mail_password = apps.get_app_config('craft').EMAIL_HOST_PASSWORD

    sender = apps.get_app_config('craft').EMAIL_FROM
    receivers = ['yuhuachang@baicmotor.com']

    message = MIMEText('python 通知', 'plain')
    message['From'] = Header('156034398@qq.com')
    message['To'] = Header('yuhuachang@baicmotor.com')

    subject = 'python smtp 邮件通知'
    message['Subject'] = Header(subject)

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, mail_port)
        # smtpObj.connect(mail_host, 465)
        smtpObj.set_debuglevel(1)
        smtpObj.login(mail_user, mail_password)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 邮件发送错误。")

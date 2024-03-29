import smtplib
from datetime import date
from email.header import Header
from email.mime.text import MIMEText
from django.apps import apps
from django.core.mail import send_mail
from craft.utils import ConnectSqlite
from django.conf import settings
import pandas as pd
from daily_focus.models import Focus, Station, Line
import datetime
from django.contrib.auth.models import User

#todo: 调用django自带sendmail未成功，用错误的密码和帐户也会正常返回1.不报错。
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

    def build_message():
        '''
        建立邮件内容message
        :return:
        '''
        mail_from = apps.get_app_config('craft').EMAIL_FROM
        mail_to = apps.get_app_config('craft').EMAIL_TO

        todays_query_set = Focus.objects.filter(focus_end__gt=datetime.date.today()).order_by('focus_end')
        df = pd.DataFrame(todays_query_set.values())

        focus_stations_list = [today.station.name for today in todays_query_set]
        counts = len(focus_stations_list)

        df['user'] = df.loc[:, 'user_id'].apply(lambda x: User.objects.get(id=x))
        df['station'] = df.loc[:, 'station_id'].apply(lambda x: Station.objects.get(id=x))
        df['line'] = df.loc[:, 'station_id'].apply(lambda x: Station.objects.get(id=x).line)

        del df['user_id']
        del df['station_id']
        del df['created']
        del df['last_modify']

        replace_columns = {
            'focus_content':'关注详情',
            'focus_start': '关注开始',
            'focus_end': '关注结束',
            'user': '发布人',
            'station': '工位',
            'line': '线体',
        }
        df.rename(columns=replace_columns, inplace=True)

        message_content = ''''''
        message_content += f'<h2><a href="http://10.36.8.159:8000">今日关注</a>共<strong>{counts}</strong>项</h2>'

        foucs_stations_string = ';'.join(focus_stations_list)
        message_content += f'<p>涉及到工位有——【{foucs_stations_string}】<br> 详情如下表</p> <br>'

        message_content += df.to_html()

        message = MIMEText(message_content, 'html')

        message['From'] = Header(mail_from)
        message['To'] = Header(mail_to)
        today = date.today().isoformat()
        subject = f'今日关注-{today}'
        message['Subject'] = Header(subject)

        return message

    mail_host = apps.get_app_config('craft').EMAIL_HOST
    mail_port = apps.get_app_config('craft').EMAIL_PORT
    mail_user = apps.get_app_config('craft').EMAIL_HOST_USER
    mail_password = apps.get_app_config('craft').EMAIL_HOST_PASSWORD
    mail_to_address = apps.get_app_config('craft').EMAIL_TO_ADDRESS

    sender = apps.get_app_config('craft').EMAIL_FROM
    receivers = mail_to_address

    message = build_message()

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, mail_port)
        smtpObj.set_debuglevel(1)
        smtpObj.login(mail_user, mail_password)
        smtpObj.sendmail(sender, receivers, message.as_string())
        smtpObj.quit()
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 邮件发送错误。")


def run_apscheduler():
    '''
    随服务器自动运行定时任务
    :return:
    '''
    from apscheduler.schedulers.background import BackgroundScheduler
    from django_apscheduler.jobstores import MemoryJobStore
    try:
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(MemoryJobStore(), 'default') #todo:用DjangoJobStore()会把调动信息存入数据库，不过容易报警。

        scheduler.add_job(send_mail_self, 'cron', hour='00', minute='15', id='send_mail_everyday', misfire_grace_time=3600, replace_existing=True)
        scheduler.start()
    except Exception as e:
        print(e)
        scheduler.shutdown()

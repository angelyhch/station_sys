# app 级别程序配置

from django.apps import AppConfig


class CraftConfig(AppConfig):
    name = 'craft'
    version = 0.1

    # 发送邮件设置
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    # SMTP地址
    EMAIL_HOST = 'smtp.qq.com'
    # SMTP端口
    EMAIL_PORT = 465
    # 自己的邮箱
    EMAIL_HOST_USER = '156034398@qq.com'
    # 自己的邮箱授权码，非密码
    EMAIL_HOST_PASSWORD = 'vjaezidbvhgscbaa'
    EMAIL_SUBJECT_PREFIX = '[station_sys]'
    # 与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false
    EMAIL_USER_TLS = True
    EMAIL_FROM = '156034398@qq.com'

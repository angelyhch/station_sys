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
    EMAIL_TO = '今日关注接收群组'
    EMAIL_TO_ADDRESS = ['yuhuachang@baicmotor.com',]
    EMAIL_TO_ADDRESS += ['fanyanling@baicmotor.com',
                        'wangweiping@baicmotor.com',
                        'huangxilong@baicmotor.com',
                        'xieguangjun@baicmotor.com',
                        'shenxiaolong@baicmotor.com',
                        'wangkuanding@baicmotor.com',
                        'huangyongquan@baicmotor.com',
                        'liangpeng@baicmotor.com',] #保障科
    EMAIL_TO_ADDRESS +=['zhanglixiang@baicmotor.com',
                        'shijiancheng@baicmotor.com',
                        'wangyuhui@baicmotor.com',
                        'zhouchudong@baicmotor.com',
                        'chennanrong@baicmotor.com'] # 车间
    EMAIL_TO_ADDRESS += ['zhuhongan@baicmotor.com',
                         'zhangwantao@baicmotor.com'] #部门领导
    EMAIL_TO_ADDRESS += ['liwenjuan01@baicmotor.com',
                         'laijinsi@baicmotor.com',
                         'guoyizhong@baicmotor.com']    #python交流
    EMAIL_TO_ADDRESS += ['liumingyang@baicmotor.com',
                         'xiaowu@baicmotor.com']    #IT支持

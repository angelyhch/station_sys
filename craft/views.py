from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
import pandas as pd
from .utils import ConnectSqlite

#todo: 下面这条语句不能放在这里，否则会导致sqlite 线程错误
# db_station = ConnectSqlite()


def home(request):
    pass
    return HttpResponse('home')


def temp3(request):
    '''
    html元素形式建立表格
    :param request:
    :return:
    '''
    db_station = ConnectSqlite()
    df = db_station.read_table('co2_view')
    header_list = df.columns.tolist()
    body_data = df.values.tolist()
    return render(request, 'craft/temp3.html',
                  {
                      'header_list': header_list,
                      'body_data': body_data
                  })



def temp2(request):
    '''
    df.to_html() 方式传递数据，暂未找到快捷转换成bootstrap-table的方式
    :param request:
    :return:
    '''
    db_station = ConnectSqlite()
    df = db_station.read_table('co2_view')
    df_html = df.to_html()
    return render(request, 'craft/temp2.html',
                  {
                      'df_data': df_html
                  })


def temp1(request):
    '''
    Json 方式传递数据， #todo:生成和解析json文件时会出现报错
    :param request:
    :return:
    '''
    db_station = ConnectSqlite()
    df = db_station.read_table('jig_view')
    header_list = df.columns.tolist()
    body_data_list = df.to_json(orient='records')
    return render(request, 'craft/temp1.html',
                  {
                      'header': header_list,
                      'body_data': body_data_list
                  })



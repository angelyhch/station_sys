from django.shortcuts import render, reverse
# Create your views here.
from django.http import HttpResponse
from craft.utils import ConnectSqlite
from .utils import suffix_view

#todo: 下面这条语句不能放在这里，否则会导致sqlite 线程错误
# db_station = ConnectSqlite()


def home(request, parameter='default'):
    pass
    return HttpResponse(f'home- {parameter}')


def station_info(request, station='W1FF4-010'):
    '''
    显示工位信息明细
    :return:
    '''
    station_upper = station.upper()
    db_station = ConnectSqlite()
    table_list_df = db_station.read_table('table_list')
    table_instation_list = table_list_df[table_list_df['is_instation'] == 1]['name'].to_list()

    station_dict = {}
    for xiangmu in table_instation_list:
        table_df = db_station.read_table(xiangmu)
        xiangmu_st_df = table_df[table_df['station'] == station_upper]
        station_dict[xiangmu] = xiangmu_st_df


    table_instation_list.sort(key=lambda x: station_dict[x].shape[0], reverse=True)
    return render(request, 'craft/station_info.html',
                  {
                      'table_instation_list': table_instation_list,
                      'station_dict': station_dict,
                  })





def stations(request):
    '''
    显示工位清单目录以及汇总信息
    :param request:
    :return:
    '''
    pass
    db_station = ConnectSqlite()
    df_station = db_station.read_table('station')
    df_station_weight = db_station.read_table('view_station_weight')


    return render(request, 'craft/stations.html',
                  {
                      'df_station': df_station,
                      'df_station_weight': df_station_weight,
                  })


def table_display(request, table_name='station'):
    '''
    展示各个表格的内容
    :param request:
    :param table_name:
    :return:
    '''
    table_view_name = suffix_view(table_name)
    db_station = ConnectSqlite()
    df = db_station.read_table(table_view_name)
    header_list = df.columns.tolist()
    body_data = df.values.tolist()

    df_table_list = db_station.read_table('table_list')
    table_name_mingcheng = df_table_list.loc[df_table_list['name'] == table_name]['mingcheng'].values[0]

    return render(request, 'craft/table_display.html',
                  {
                      'header_list': header_list,
                      'body_data': body_data,
                      'table_name_mingcheng': table_name_mingcheng
                  })



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



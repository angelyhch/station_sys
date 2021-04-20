from django.shortcuts import render, reverse
# Create your views here.
from django.http import HttpResponse
from craft.utils import ConnectSqlite
from .utils import suffix_view
import logging
logger = logging.getLogger()
sh = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
FORMAT = '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
formatter = logging.Formatter(FORMAT)
sh.setFormatter(formatter)

logger.addHandler(sh)

#todo: 下面这条语句不能放在这里，否则会导致sqlite 线程错误
# db_station = ConnectSqlite()


def home(request):
    pass
    return render(request, 'craft/home.html')


def table_display_insert(request):
    import json
    recv_data = json.loads(request.body)
    row_data = recv_data['row_data']
    table_name = recv_data['table_name']
    db_station = ConnectSqlite()
    sql = ConnectSqlite.build_sql(table_name, row_data, operate='insert')
    db_station.insert_update_table(sql)
    logger.info(sql)
    return HttpResponse(str(recv_data))

def table_display_edit(request):
    import json
    recv_data = json.loads(request.body)
    row_data = recv_data['row_data']
    table_name = recv_data['table_name']
    db_station = ConnectSqlite()
    sql = ConnectSqlite.build_sql(table_name, row_data, operate='update')
    db_station.insert_update_table(sql)
    logger.info(sql)
    return HttpResponse(str(recv_data))


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

    if request.user.is_authenticated:
        template_name = 'craft/table_display_user.html'
    else:
        template_name = 'craft/table_display_guest.html'

    return render(request, template_name,
                  {
                      'header_list': header_list,
                      'body_data': body_data,
                      'table_name': table_name,
                      'table_name_mingcheng': table_name_mingcheng
                  })



from django.shortcuts import render, reverse
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from craft.utils import ConnectSqlite, logger
from .utils import suffix_view
import json
from daily_focus.models import Focus, Station
from daily_focus.forms import FocusForm, StationForm

#todo: 下面这条语句不能放在这里，否则会导致sqlite 线程错误
# db_station = ConnectSqlite()


def home(request):
    pass
    return render(request, 'craft/home.html')


def foucs_history(request):
    pass
    db_station = ConnectSqlite()
    df = db_station.read_table('daily_foucs')
    header_list = df.columns.tolist()
    body_data = df.values.tolist()
    return render(request, 'craft/foucs_history.html',
                  {
                      'header_list': header_list,
                      'body_data': body_data,
                  }
                  )


def daily_foucs(request):
    db_station = ConnectSqlite()
    df = db_station.read_table('daily_foucs_view')

    station_table_df = db_station.read_table('station')
    line_list = list(set(station_table_df['生产线']))
    line_station_dict = {}
    for line in line_list:
        stations = station_table_df[station_table_df['生产线'] == line]['station'].to_list()
        line_station_dict[line] = stations

    header_list = df.columns.tolist()
    body_data = df.values.tolist()
    return render(request, 'craft/daily_foucs.html',
                  {
                      'header_list': header_list,
                      'body_data': body_data,
                      'line_list': line_list,
                      'line_station_dict': line_station_dict,
                  }
                  )


def part_info(request, lingjianhao):
    '''
    显示零件号对应的bom信息
    :param request:
    :param lingjianhao:
    :return:
    '''
    db_station = ConnectSqlite()
    pbom_df = db_station.read_table('pbom_view')
    part_info_df = pbom_df[pbom_df['lingjianhao']==lingjianhao]

    return render(request, 'craft/part_info.html',
                  {'part_info_df':part_info_df}
                  )

def table_display_insert(request):
    recv_data = json.loads(request.body)
    row_data = recv_data['row_data']
    table_name = recv_data['table_name']
    db_station = ConnectSqlite()
    sql = ConnectSqlite.build_sql(table_name, row_data, operate='insert')
    db_station.insert_update_table(sql)
    logger.info(sql)
    return HttpResponse(str(recv_data))


def table_display_edit(request):
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
    table_list_df = db_station.read_table('table_list_view')
    table_instation_list = table_list_df[table_list_df['is_instation'] == 1]['name'].to_list()

    station_dict = {}
    for xiangmu in table_instation_list:
        table_df = db_station.read_table(xiangmu)
        xiangmu_st_df = table_df[table_df['station'] == station_upper]
        station_dict[xiangmu] = xiangmu_st_df

    controlplan_df = db_station.read_table('controlplan_view')
    table_instation_list.sort(key=lambda x: station_dict[x].shape[0], reverse=True)
    return render(request, 'craft/station_info.html',
                  {
                      'table_instation_list': table_instation_list,
                      'station_dict': station_dict,
                      'controlplan_df': controlplan_df,
                  })


def stations(request):
    '''
    显示工位清单目录以及汇总信息
    :param request:
    :return:
    '''
    pass
    db_station = ConnectSqlite()
    df_station = db_station.read_table('station_view')
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

    df_table_list = db_station.read_table('table_list_view')
    table_name_mingcheng = df_table_list.loc[df_table_list['name'] == table_name]['mingcheng'].values[0]

    return render(request, 'craft/table_display_guest.html',
                  {
                      'header_list': header_list,
                      'body_data': body_data,
                      'table_name': table_name,
                      'table_name_mingcheng': table_name_mingcheng
                  })


@login_required
def table_display_user(request, table_name='station'):
    '''
    进入后台编辑模式
    :param request:
    :param table_name:
    :return:
    '''

    focus_form = FocusForm()

    table_view_name = suffix_view(table_name)
    db_station = ConnectSqlite()
    df = db_station.read_table(table_view_name)
    header_list = df.columns.tolist()
    body_data = df.values.tolist()

    station_table_df = db_station.read_table('station')
    line_list = list(set(station_table_df['生产线']))
    line_station_dict = {}
    for line in line_list:
        stations = station_table_df[station_table_df['生产线'] == line]['station'].to_list()
        line_station_dict[line] = stations


    df_table_list = db_station.read_table('table_list_view')
    table_name_mingcheng = df_table_list.loc[df_table_list['name'] == table_name]['mingcheng'].values[0]

    return render(request, 'craft/table_display_user.html',
                  {
                      'header_list': header_list,
                      'body_data': body_data,
                      'table_name': table_name,
                      'table_name_mingcheng': table_name_mingcheng,
                      'line_list': line_list,
                      'line_station_dict': line_station_dict,
                      'focus_form': focus_form,
                  })


from craft.emails import run_apscheduler
run_apscheduler()

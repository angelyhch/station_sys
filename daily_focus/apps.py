from django.apps import AppConfig
from craft.utils import ConnectSqlite


# 线体清单和线体工位字典
def get_line_station():
    db_station = ConnectSqlite()
    station_table_df = db_station.read_table('station')
    line_list = list(set(station_table_df['生产线']))
    line_station_dict = {}
    for line in line_list:
        stations = station_table_df[station_table_df['生产线'] == line]['station'].to_list()
        line_station_dict[line] = stations
    return line_list, line_station_dict


class DailyFocusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'daily_focus'
    LINE_LIST, LINE_STATION_DICT = get_line_station()

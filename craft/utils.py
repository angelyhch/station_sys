import sys
import pandas as pd
import os
import sqlite3
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

import logging
logger = logging.getLogger()
sh = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
FORMAT = '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
formatter = logging.Formatter(FORMAT)
sh.setFormatter(formatter)
logger.addHandler(sh)


# todo:??
# sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/' + '..')
# sys.path.append('..')


class ConnectSqlite:
    def __init__(self, dbName=settings.BASE_DIR / 'db3_station.sqlite3'):
        '''
        初始化连接
        :param dbName: 连接数据库的路径名
        '''

        self._conn = sqlite3.connect(dbName)
        self._cur = self._conn.cursor()
        self._time_now = '[' + sqlite3.datetime.datetime.now().strftime('%Y%m%d %H%M%S') + ']'

    def get_conn(self):
        return self._conn

    def get_cur(self):
        return self._cur

    def read_table(self, table_name):
        '''
        读取表格数据
        :param table_name:
        :return: dataframe 格式数据
        '''
        sql = f'select * from {table_name}'
        df = pd.read_sql(sql, self._conn)
        return df

    def excel_to_table(self, read_excel_name, to_table_name, temp_folder=r"static\craft_temp_data",
                       header=0, index_col=None):
        # 设定读取数据源地址
        excel_path = os.path.join(settings.BASE_DIR, temp_folder, read_excel_name)
        # 读取EXCEL数据
        df1 = pd.read_excel(excel_path, header=header, index_col=index_col)
        # EXCEL数据写入数据库
        df1.to_sql(to_table_name, self._conn, if_exists='replace')

    def close_con(self):
        '''
        关闭连接对象，主动调用
        :return:
        '''
        self._cur.close()
        self._conn.close()

    def create_table(self, sql):
        '''
        创建表初始化
        :param sql: 建表语句
        :return: True is ok
        '''

        try:
            self._cur.execute(sql)
            self._conn.commit()
            return True
        except Exception as e:
            print(self._time_now, '[create table error]', e)
            return False

    def drop_table(self, table_name):
        '''
        删除表
        :param table_name:表名
        :return:
        '''

        try:
            self._cur.execute(f'drop table {table_name}')
            self._conn.commit()
            return True
        except Exception as e:
            print(self._time_now, '[drop table error]', e)
            return False

    def delete_table(self, sql):
        '''
        删除表记录
        :param sql:
        :return: True or False
        '''

        try:
            if 'delete' in sql.lower():
                self._cur.execute(sql)
                self._conn.commit()
                return True
            else:
                print(self._time_now, '[execute sql is not delete]')
                return False
        except Exception as e:
            print(self._time_now, '[delete table error]', e)
            return False

    def fetchall_table(self, sql, limit_flag=True):
        '''
        查询所有数据
        :param sql:
        :param limit_flag: False 查询一条， True查询全部
        :return:
        '''

        try:
            self._cur.execute(sql)
            war_msg = self._time_now + f'The [{sql}] is empty or equal None!'
            if limit_flag is True:
                r = self._cur.fetchall()
                return r if len(r) > 0 else war_msg
            elif limit_flag is False:
                r = self._cur.fetchone()
                return r if len(r) > 0 else war_msg
        except Exception as e:
            print(self._time_now, '[select table error', e)

    @staticmethod
    def build_sql(table_name, data, operate='update'):
        '''
        建立sql语句字符串
        :param table_name: 表格名称
        :param data: update-字典，delete-删除条件,insert-单行数据元组
        :param operate:update, delete, insert
        :return:
        '''

        def right_replace(string, old, new, max_counts=1):
            '''
            字符串从右向左替换字符，并可以指定数量，重写原replace 函数
            :param string:
            :param old:
            :param new:
            :param max_counts:
            :return:
            '''
            return string[::-1].replace(old[::-1], new[::-1], max_counts)[::-1]

        data_dict = data
        if operate == 'update':
            update_table = f' update {table_name} '

            set_col = f'set '
            for key, value in data_dict.items():
                set_col += f" {key}='{value}', " if key != 'index' else " "
            set_col = right_replace(set_col, ",", "")

            where_condition = f" where [index]='{data_dict['index']}' "

            result_sql = update_table + set_col + where_condition
        elif operate == 'insert':
            insert_table = f" insert into {table_name}  "

            cols_in = ''
            values_in = ''
            for (key, value)  in data_dict.items():
                cols_in += f'{key}, ' if key != 'index' else f' [{key}], '
                values_in += f'"{value}", ' if key != 'index' else f' (select count([index]) from {table_name}) + 1 , '
            cols_in = right_replace(cols_in, ',', '')
            values_in = right_replace(values_in, ',', '')
            cols = f" ({cols_in}) "
            values = f" ({values_in}) "

            result_sql = insert_table + cols + 'values ' + values

        elif operate == 'delete':
            pass
        else:
            raise #参数错误


        return result_sql

    def insert_update_table(self, sql):
        '''
        插入更新表格记录
        :param sql:
            sql_insert = "insert into linetoclass values('index06', 'line06', 'class06')"
            sql_delete = "delete from linetoclass where [index]='index04'"
            sql_update = "update linetoclass set  生产线='line05', 班组='class05' where [index]='index03'"
        :return:
        '''

        try:
            self._cur.execute(sql)
            self._conn.commit()
            return True
        except Exception as e:
            print(self._time_now, '[insert/update table error:', e)
            return False

    def insert_table_many(self, sql, value):
        '''
        插入多条记录
        :param sql: [(), ()]
        :param value:
        :return:
        '''

        try:
            self._cur.executemany(sql, value)
            self._conn.commit()
            return True
        except Exception as e:
            print(self._time_now, '[insert many table error')
            return False


def set_craft_global():
    '''
    设定 craft app 应用级别的全局变量，在settings的 templates 配置 context—processes中注册该函数
    :param request:
    :return:
    '''
    db = ConnectSqlite()
    table_list_df = db.read_table('table_list_view')
    table_list_display = table_list_df[table_list_df['is_display'] == 1]['name'].to_list()

    station_df = db.read_table('station_view')
    station_name_dict = dict(zip(station_df['station'], station_df['工位名称']))

    station_list = station_df['station'].to_list()
    craft_global = {
        'craft_table_list': table_list_df,
        'craft_station_list': station_list,
        'station_name_dict': station_name_dict,
    }

    return craft_global


def suffix_view(table_name):
    '''
    add suffix 'view' end with table_name.
    在table_name后面增加 view 后缀名，用于调用数据库中view表格，实现原始数据与应用数据的解耦
    :param table_name:
    :return:
    '''

    return table_name + '_view'


# db_station = ConnectSqlite()
if __name__ == '__main__':
    db = ConnectSqlite()
    dt = {'index':'v1', 'k2':'v2', 'k3':'v3'}

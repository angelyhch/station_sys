import sys
import pandas as pd
import os
import sqlite3
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# todo:??
# sys.path.append(os.path.abspath(os.path.dirname(__file__)) + '/' + '..')
# sys.path.append('..')


class ConnectSqlite:
    def __init__(self, dbName=settings.BASE_DIR/'db3_station.sqlite3'):
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
        df1.to_sql(to_table_name, self._conn,  if_exists='replace')  # todo: 以后要和三坐标分析拆分数据库或者拆表

    def close_con(self):
        '''
        关闭连接对象，主动调用
        :return:
        '''
        self._cur.close()
        self._conn.close()

    def create_table(self,sql):
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
            print(self._time_now, '[delete table error]',e)
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
                return r if len(r)>0 else war_msg
            elif limit_flag is False:
                r = self._cur.fetchone()
                return r if len(r)>0 else war_msg
        except Exception as e:
            print(self._time_now, '[select table error', e)

    def insert_update_table(self, sql):
        '''
        插入更新表格记录
        :param sql:
        :return:
        '''

        try:
            self._cur.execute(sql)
            self._conn.commit()
            return True
        except Exception as e:
            print(self._time_now, '[insert/update table error')
            return False

    def insert_table_many(self, sql, value):
        '''
        插入多条记录
        :param sql: [(), ()]
        :param value:
        :return:
        '''

        try:
            self._cur.executemany(sql,value)
            self._conn.commit()
            return True
        except Exception as e:
            print(self._time_now, '[insert many table error')
            return False


def set_craft_global(request):
    '''
    设定 craft app 应用级别的全局变量，在settings的 templates 配置 context—processes中注册该函数
    :param request:
    :return:
    '''
    db = ConnectSqlite()
    table_list_df = db.read_table('table_list')
    table_list_display = table_list_df[table_list_df['is_display'] == 1]['name'].to_list()

    craft_global = {
        'table_list_display': table_list_display,
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
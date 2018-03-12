#coding=utf-8
#@author: Zengliangwei
#mysql的基本操作模块

import os,MySQLdb
import MySQLdb.cursors

class connector:

    conn = None
    cursor = None

    #mysql的配置读取及连接
    def __init__(self):
        fp = open(os.path.dirname(os.path.realpath(__file__))+'/mysql.config', 'r')
        dic = {}
        for eachline in fp:
            lineitem = eachline.strip().split('=')
            dic[lineitem[0]] = lineitem[1]
        fp.close()
        try:
            self.conn = MySQLdb.connect(host=dic['host'],user=dic['user'],passwd=dic['passwd'],port=int(dic['port']),db=dic['db'],charset="utf8",cursorclass = MySQLdb.cursors.DictCursor)
            self.cursor = self.conn.cursor()
        except:
            print 'database connection fail, check the mysql configure.'
            exit(1)
        print 'connect database success!'

    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        print 'database connection closed.'

    #清空数据库表数据
    def truncate(self, table):
        sql = 'truncate table %s'
        sql = sql % table
        self.cursor.execute(sql)
        self.conn.commit()

    #批量插入数据
    def insert(self, table, param_list, value_list):
        sql = 'insert into %s(%s) values (%s)'
        value_str = ''
        for i in range(len(param_list)):
            if i == 0:
                value_str += '%s'
            else:
                value_str += ', %s'
        sql = sql % (table, ','.join(param_list), value_str)
        self.cursor.executemany(sql,value_list)
        self.conn.commit()

    def insertDict(self, table, param_list, dic_list):
        value_list = []
        for dic in dic_list:
            value = []
            for param in param_list:
                if param not in dic:
                    value.append(None)
                else:
                    value.append(dic[param])
            value_list.append(value)
        self.insert(table, param_list, value_list)

    #搜索数据库记录
    def searchone(self, table, param_list, condition = '1'):
        sql = 'select %s from %s where %s limit 1'
        sql = sql % (','.join(param_list), table, condition)
        self.cursor.execute(sql)
        return self.cursor.fetchone()
        
    def searchall(self, table, param_list, condition = '1'):
        sql = 'select %s from %s where %s'
        sql = sql % (','.join(param_list), table, condition)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    #更新数据库记录
    def update(self, table, param_dic, condition = '1'):
        sql = 'update %s set %s where %s'
        value_list = []
        value_str = ''
        i = 0
        for param_name in param_dic:
            value_list.append(param_dic[param_name])
            if i == 0:
                value_str += param_name + '=%s'
            else:
                value_str += ', '+param_name + '=%s'
            i += 1
        sql = sql % (table, value_str, condition)
        self.cursor.execute(sql,value_list)
        self.conn.commit()

    #删除数据库记录
    def delete(self, table, condition = '1'):
        sql = 'delete from %s where %s'
        sql = sql % (table, condition)
        self.cursor.execute(sql)
        self.conn.commit()
        
if __name__ == '__main__':
    conn = connector()
    result = conn.searchall('ipmarker_data',['region_name'], 'country_name = "中国" group by region_name')
    conn.close()
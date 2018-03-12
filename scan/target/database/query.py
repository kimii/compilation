#coding=utf-8
#@author: Zengliangwei

import os,sys
import operate
from ipaddress.ipaddress import *

class query:

    connector = None
    current_id = 0
    count = 0
    total_count = 0

    def __init__(self):
        print 'init query module.'
        self.connector = operate.connector()

    def close(self):
        self.connector.close()
        print 'close query module.'

    #通过ip地址查询对应数据库表地理信息记录
    def ipQuery(self, table, param_list, ip):
        ip_from_mark = 0
        if 'ip_from' in param_list:
            ip_from_mark = 1
        else:
            param_list.append('ip_from')
        if type(ip) == type('') or type(ip) == type(u''):
            ipnum = ip2int(ip)
        else:
            ipnum = ip
        condition = 'ip_to >= %d' % ipnum
        result = self.connector.searchone(table, param_list, condition)
        if result == None:
            result = {}
        elif result['ip_from'] > ipnum:
            result = {}
        if ip_from_mark == 0:
            param_list.remove('ip_from')
        return result

    def multiIpQuery(self, table, param_list, ip_list):
        result_list = []
        for ip in ip_list:
            result = self.ipQuery(table, param_list, ip)
            tmplist = [ip,result]
            result_list.append(tmplist)
        return result_list

    def fastIpQuery(self, table, param_list, ip):
        ip_from_mark = 0
        id_mark = 0
        if 'ip_from' in param_list:
            ip_from_mark = 1
        else:
            param_list.append('ip_from')
        if 'id' in param_list:
            ip_from_mark = 1
        else:
            param_list.append('id')
        if type(ip) == type('') or type(ip) == type(u''):
            ipnum = ip2int(ip)
        else:
            ipnum = ip
        condition = 'id >= %d and ip_to >= %d' % (self.current_id, ipnum)
        result = self.connector.searchone(table, param_list, condition)
        if result == {} or result == None:
            result = {}
            return result
        elif result['ip_from'] > ipnum:
            result = {}
            return result
        self.current_id = result['id']
        if id_mark == 0:
            param_list.remove('id')
        if ip_from_mark == 0:
            param_list.remove('ip_from')
        return result

    def fastMultiIpQuery(self, table, param_list, ip_list):
        self.count = 0
        self.total_count = len(ip_list)
        ip_num_list = []
        for ip in ip_list:
            ipnum = ip2int(ip)
            ip_num_list.append(ipnum)
        ip_num_list.sort()
        self.current_id = 0
        result_list = []
        for ipnum in ip_num_list:
            result = self.fastIpQuery(table, param_list, ipnum)
            tmplist = [int2ip(ipnum),result]
            result_list.append(tmplist)
            self.count += 1
        print 'completed.'
        return result_list

    #直接请求对应数量的数据库表地理信息记录
    def recordQuery(self, table, param_list, offset, length):
        condition = 'id >= %d limit %d' % (offset, length)
        return self.connector.searchall(table, param_list, condition)


if __name__ == "__main__":
    import time

    start_time = time.time()
    myFile = open('600000_ip.txt','r')
    iplist = myFile.read().split("\n")
    i = 0
    while i < len(iplist):
        iplist[i] = iplist[i].strip()
        if iplist[i] == "":
            del iplist[i]
            continue
        i += 1
    data = ""
    queryObj = query()
    resultlist1 = queryObj.fastMultiIpQuery('ip2location_data',["ip_from","ip_to","country_code","country_name","region_name","city_name","isp_name","domain_name"],iplist)
    queryObj.close()
    print time.time() - start_time
    myFile.close()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from restful import settings
import pymysql


class MySQL:
    __db = None

    # 在这里配置自己的SQL服务器
    __config = {
        'host': settings.MYSQL_HOST,
        'port': settings.MYSQL_PORT,
        'username': settings.MYSQL_USER,
        'password': settings.MYSQL_PASSWORD,
        'database': settings.MYSQL_DB,
        'charset': settings.MYSQL_CHARSET
    }

    def __init__(self):
        self.__connect()

    def __del__(self):
        if self.__db is not None:
            self.__db.close()

    def __connect(self):
        if self.__db is None:
            self.__db = pymysql.connect(
                host=self.__config['host'],
                port=self.__config['port'],
                user=self.__config['username'],
                passwd=self.__config['password'],
                db=self.__config['database'],
                charset=self.__config['charset']
            )
        return self.__db

    '''
    直接使用sql查询
    sql = "SELECT stu_uid FROM student WHERE id="+id
    result = database.query(sql)
    '''
    def query(self,_sql):
        cursor = self.__connect().cursor()
        try:
            cursor.execute(_sql)
            data = cursor.fetchall()
            # 提交到数据库执行
            self.__connect().commit()
        except:
            # 如果发生错误则回滚
            self.__connect().rollback()
            return False
        return data

    '''
    各种操作说明
    1. 查询操作
        result = database.query_dic({
            'select': 'stu_uid',
            'from': 'student',
            'where': {
                'id':id，
                'iii':3
            }
        })
    2. 复杂的where条件
        result = database.query_dic({
            'select': 'stu_uid',
            'from': 'student',
            'where': "id>2 and id<5"
        })
    3. 删除操作
        result = database.query_dic({
           'delete': 'student',
           'where': "iii>5"
        })
    4. 插入操作
        database.query_dic({
            'insert': 'student',
            'domain_array':[
                'stu_uid', 'iii'
            ],
            'value_array':[
                'asdf',33232
            ]
        })
    '''
    def query_dic(self,_sql_dic):
        if 'select' in _sql_dic.keys():
            sql = "SELECT "+_sql_dic['select']+" FROM "+_sql_dic['from']+self.where(_sql_dic['where'])
            return self.query(sql)
        elif 'insert' in _sql_dic.keys():
            sql = "INSERT INTO "+_sql_dic['insert']+self.quote(_sql_dic['domain_array'],type_filter=False)+" VALUES "+self.quote(_sql_dic['value_array'])
            return self.query(sql)
        elif 'replace' in _sql_dic.keys():
            sql = "REPLACE INTO "+_sql_dic['replace']+self.quote(_sql_dic['domain_array'],type_filter=False)+" VALUES "+self.quote(_sql_dic['value_array'])
            return self.query(sql)
        if 'delete' in _sql_dic.keys():
            sql = "DELETE FROM " + _sql_dic['delete'] + self.where(_sql_dic['where'])
            return self.query(sql)


    def where(self, _sql):
        if(isinstance(_sql,dict)==False):
            return " WHERE "+ str(_sql)
        if(isinstance(_sql,dict)):
            _sql_dic = _sql
            s = " WHERE "
            index = 0
            for domain in _sql_dic:
                if(index==0):
                    s += domain+"="+ str(_sql_dic[domain]) +" "
                    index+=1
                else:
                    s += "AND "+domain + "=" + str(_sql_dic[domain]) + " "
            return s

    # 为数组加上外括号，并拼接字符串
    def quote(self, _data_array, type_filter=True):
        s = "("
        index = 0
        if(type_filter):
            for domain in _data_array:
                if(index==0):
                    if (isinstance(domain, str)):
                        s += "'" + domain + "'"
                    else:
                        s += str(domain)
                    index+=1
                else:
                    if (isinstance(domain, str)):
                        s += ", " + "'" + domain + "'"
                    else:
                        s += ", " + str(domain)
        else:
            s += ','.join(_data_array)

        return s+")"

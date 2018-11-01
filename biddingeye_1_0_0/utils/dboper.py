# coding=utf-8
import MySQLdb

conn = MySQLdb.connect(
                    host='192.168.8.101',
                    port=3306,
                    user='root',
                    passwd='123456',
                    db='mysql',
                )
cur = conn.cursor()
cur.execute("insert into be_ori_notice values(2004, '辽宁移动',2,'公告', '2017-03-18', 'urlxxx', 'year 2 class','2017-3-18')".encode("utf8"))
cur.close()
conn.commit()
conn.close()


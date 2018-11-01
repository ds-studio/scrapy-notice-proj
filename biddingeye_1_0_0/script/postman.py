# coding=utf-8
import ConfigParser
import datetime

import os
import re

from biddingeye_1_0_0.classify.classify_filter import ClassifyMan
#import ClassifyMan

import MySQLdb
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cStringIO import StringIO
from platform import python_version
from smtplib import SMTP
import time

import sys


reload(sys)
sys.setdefaultencoding('utf8')

# SMTP_SSL added in 2.6, fixed in 2.6.3
#import MAILBOX as MAILBOX

release = python_version()
if release > '2.6.2':
    from smtplib import SMTP_SSL, SMTPServerDisconnected
else:
    SMTP_SSL = None


class postman():
        name = 'BiddingEye'
        def __init__(self):
                self._db_dict = {
                                 "host":"10.10.126.127",
                                 "port": 3306,
                                 "user": "Bee",
                                 "passwd": "Bee#123456",
                                 "database": "bee",
                                 "charset":"utf8"
                                 }
                self._db_handle = None
                self._key_words =[]
                self._mail_users = None

                self._mail_title = ""
                self._mail_content = ""

                self._user = ""
                self._passwd = ""

                self._timelist = ""
                self._maillist = ""

                self.initDBData()
                self.initNotifyData()


        def initDBData(self):
            try:
                print self._db_dict['host'] + "|" + str(self._db_dict['port']) + "|" +  self._db_dict['user'] + \
                "|" + self._db_dict['passwd'] + "|" + self._db_dict['database'] + "|" + self._db_dict['charset']

                conn = MySQLdb.connect(host=self._db_dict["host"], port=self._db_dict["port"], user=self._db_dict["user"],
                                       passwd=self._db_dict["passwd"], db=self._db_dict["database"], charset=self._db_dict["charset"])

            except MySQLdb.Error, e:
                try:
                    sqlError = "Error %d:%s" % (e.args[0], e.args[1])
                    print sqlError
                except IndexError:
                    print "MySQL Error:%s" % str(e)
                return

            self._db_conn = conn
            self._db_cursor = conn.cursor()


        def initNotifyData(self):
            cp = ConfigParser.SafeConfigParser()
            cp.read('../conf/setup.conf')
            self._db_handle = cp.items('db')

            cp.read('../conf/notify.conf')
            #self._key_words = cp.items('keyword')
            self._mail_users = cp.items('mailaddr')

            self._user = cp.get("userinfo", "user")
            self._passwd = cp.get("userinfo", "passwd")
            self._key_words = cp.get("keyword", "keylist1").split('|')

            print self._mail_users
            print self._user + "|" + self._passwd
            for keyword in self._key_words:
               print "keyword:"+keyword


        def checkNoticeInfo(self):

            curr_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))

            print "time:" + str(curr_time)
            select_sql = "select id, prov, date, url, title, apply_tm from BID_PURCHASE_NOTICE_DATA_T WHERE  " \
                  "date = date_sub(curdate(), interval 1 day) and mail_time is NULL or date = curdate() and mail_time is NULL "

            #select_sql = "select id, prov, date, url, title, apply_tm from BID_PURCHASE_NOTICE_DATA_T WHERE  " \
            #             "date = '2017-05-11' or date = '2017-05-12' or date = '2017-05-13' or date = '2017-05-14'"

            print "DB UPDATE:" + str(select_sql)

            try:
                self._db_cursor.execute(select_sql)
                content_list = self._db_cursor.fetchall()
                for row  in content_list:
                    print "data:" + str(row[0]) + "|" + str(row[1]) + "|" + str(row[2]) + "|" + str(row[3] + "|" + str(row[4]))

                email = self.build_mail_text(content_list)

                #print "email: " + str(email) + "\n"
                if email != None:
                    rv = self.send_mail2(email)
                    if(rv == -1):
                        return

                for row in content_list:
                    update_sql = "update BID_PURCHASE_NOTICE_DATA_T SET mail_time='%s' WHERE id='%s' " % (curr_time, str(row[0]))
                    lineover = self._db_cursor.execute(update_sql)
                    #print "update sql:" + update_sql + " result:" + str(lineover)

            except MySQLdb.Error, e:
                sqlError = "Error %d:%s" % (e.args[0], e.args[1])
                print sqlError
                return

            self._db_conn.commit()
            self._db_cursor.close()
            self._db_conn.close()

        def build_mail_text(self, content_list):
            titletype = ""
            titlemailcnt = 0
            text_body ="""
                <table border='1' cellspacing='0' cellpadding='0' >
                    <thead>
                        <tr>
			  <th class="th-style">所属类别</th>
                          <th class="th-style">采购单位</th>
                          <th class="th-style">招标信息</th>
                          <th class="th-style">投标截止</th>
                        </tr>
                  </thead>
            """
            classifyman = ClassifyMan()
            #厂商提取
            factory_list = []
            focuslist = []
            for row in content_list:
		fetch_time = row[2]
		print "fetch time:" + str(fetch_time)
                factory = row[1]
                url = row[3]
                title = row[4]
                apply_time = row[5]
                #if classifyman2.washfilter(title) == 0:
                #     continue

                focuslist = classifyman.focusfilter(title)
                if len(focuslist) > 0:
                    # 厂商提取
                    if factory not in factory_list:
                        factory_list.append(factory)
                    titletype = ','.join(focuslist)
                    text_body = text_body + ("<tr><td>%s</td><td>%s</td><td><a href='%s' id='url_1' >%s</a></td><td>%s</td></tr>" % (titletype, factory, url, title,  apply_time))
                    print "textbody:"+text_body
		    titlemailcnt = titlemailcnt + 1


	    if titlemailcnt <= 0:
		print "无通知数据.."+"\n"
		return None

            text_body = text_body + "</table>"
            #时间提取

            #print "text_body content:"+ text_body +"\n"
            if len(text_body) <= 0:
                return
            #组装mail content
            email = MIMEMultipart('alternative')
            #text = MIMEText(u'Hello World!\r\n', 'plain')

            # text = MIMEText("", _subtype='html', _charset='UTF-8')
            # email.attach(text)

            html_head = """
                            <html lang='en'>
                            <head><title>notice</title><meta charset="UTF-8" /></head>
                            <body>
                            <h4>Bidding系统采集到最新招标数据，参考如下:</h4>
            """

            html_tail = """
                            <div style="font-weight: bold;padding: 10px 0px 0px 0px;font-size: 12px">当前分类:</div>
<div style="font-size: 12px;text-indent:25px;">传统短信,反欺诈,金融,可视化,骚扰,态势感知,脱敏,位置服务,物联网,信息安全,营销,云计算,资源池,汽车,大数据,NFV</div>
            """

            print "text_body content:" + html_head+text_body+html_tail + "\n"

            email.attach(MIMEText(html_head+text_body+html_tail, 'html', _charset='UTF-8'))

            who = '%s@neusoft.com' % self._user
            _from = who
            _to = ""

            mail_list = []
            for idx, addr in self._mail_users:
                print "收件人:"+addr
                mail_list.append(addr)

            timeinfo = time.strftime("%Y年%m月%d日%H时")

            #email['To']= ', '.join(["sun.yue@neusoft.com"])
            #email['To'] = mail_list

            #email['From'] = _from
            email['From'] = "mid-smias@neusoft.com"
            email['Subject'] = timeinfo + u" 中国移动招标信息:"+ ",".join(factory_list)


            return email

        def send_mail2(self, mail_msg):
            print "发送邮件通知 .......！"
            #print str(mail_msg)
            print "mail from:"+mail_msg['From']
            #print "mail to:" + str(mail_msg['To'])
            try:
                # s = SMTP('')
                # s.connect('smtp.neusoft.com')
                # s.starttls()

                print '*** Doing SMTP send via TLS...'
                s = SMTP('smtp.neusoft.com', 587)
                if release < '2.6':
                    s.ehlo()  # required in older releases
                #s.starttls()
                if release < '2.5':
                    s.ehlo()  # required in older releases
                #s.login(self._user, self._passwd)
                s.starttls()
                s.login('mid-smias', 'OP.m-i875*&n')
                mail_list = []
                for idx, addr in self._mail_users:
                    print "收件人:" + addr
                    mail_list.append(addr)

                mail_msg['To'] = ','.join(mail_list)
                #s.sendmail(mail_msg['From'], mail_msg['To'], mail_msg.as_string())
                # to_list=['sun.yue@neusoft.com','libk@neusoft.com']
                s.sendmail(mail_msg['From'], mail_list, mail_msg.as_string())
                s.quit()
                print "邮件发送成功"
            except Exception, e:
                print "失败" + str(e)
                return -1

        # def send_mail(self, mail_msg):
        #     print "发送邮件通知 .......！"
        #     print str(mail_msg)
        #     try:
        #         s = SMTP()
        #         s.connect('smtp.163.com')
        #         #s.starttls()
        #         #s.login(self._user, self._passwd)
        #         s.login("davidsun_home@163.com", "*****")
        #         s.sendmail(mail_msg['From'], mail_msg['To'], mail_msg.as_string())
        #         s.quit()
        #         print "邮件发送成功"
        #     except Exception, e:
        #         print "失败" + str(e)
            return 0

        def keyword_filter(self, title):
            isSend = False
            for keyword in self._key_words:
               se = re.compile(keyword)
               if se.search(str(title)):
                   isSend = True
                   print "match key:["+keyword+"] in ("+title+")"

            return isSend





if __name__ == '__main__':
    try:
        man = postman()
        man.checkNoticeInfo()

       # parser.event_list()
    except IOError,e:
        print 'IOError:', e

#!/bin/env python
# coding:utf-8

import string, re, sys
import fileinput

reload(sys)
sys.setdefaultencoding('utf8')

name_buyer = "采购人"
name_agent = "采购代理"
name_papertm = "标书购买截止时间"
name_betm = "投标截止时间"

name_budget = "项目预算"
name_ntype = "公告类型"
name_keylist = "关键字列表"
name_aptitude = "资质要求"
name_actualize = "实施内容"
name_stitle = "包标题"


class KeyWordSearch():
    def __init__(self, content):
        print "keywordsearch content len %d" % len(content)
        self._content = content
        self._buyer = re.compile("(?<=(采购人为))[^-~]+?公司(?=[，。])")
        self._agent = re.compile("(?<=(采购代理机构为))([^-~]+公司(?=[，。]))+?")

        self._tm = re.compile("(\d{2,4}年[^-~]+\d+分)+?")
        self._betm = re.compile("(纸质应答[^-~]+\d+分)+?")

        self._tm2 = re.compile("((?<=至)\d{2,4}年[^-~]+\d+分)+?")
        self._papertm = re.compile("(文件售卖[^-~]+\d+分)+?")

        self._budgetcheck = re.compile("(预算|金额|不含税)")
        self._budget = re.compile("([1-9]\d*万元.*税.{3})")
        self._ntype = re.compile("")

        self._aptitudestart = re.compile(".*[二、].*资格要求")
        self._aptitudeend = re.compile("^三、.*")

        self._actualize_tablestart = re.compile("表格X:.*")
        self._actualize_tablehead = re.compile("包段 产品名称")
        self._actualize_title = re.compile("包[0-9]{0,3} (.+?) ")
        self._stitle = re.compile("")
        self.info_dict = {
            "name_buyer": "",
            "name_agent": "",
            "name_papertm": "",
            "name_betm": "",
            "name_budget": "",
            "name_ntype": "",
            "name_keylist": "",
            "name_aptitude": "",
            "name_actualize": "",
            "name_stitle": []
        }

    def fetchHandle(self):
        title = ""
        str_buyer = ""
        str_agent = ""
        str_papertm = ""
        str_betm = ""
        str_budget = ""
        str_ntype = ""
        str_aptitude = ""
        str_actualize = ""
        str_stitle_list = []
        aptitude_flag = 0
        actualize_flag = 0
        aptitude_buf = ""
        ap_end = None
        ap_start = None

        # 内容分类
        # 子内容分类
        for line in self._content:
            # result=buyer.search("公司2016年行业网关等系统维保技术服务，采购人为中国移动通信集团辽宁有限公司，")
            if title == "":
                title = line

            # 提取采购人
            r_buyer = self._buyer.search(line)
            if r_buyer:
                # print "%-20s\t%s" % (name_buyer, r_buyer.group())
                if str_buyer == "":
                    str_buyer = r_buyer.group()

            # 提取采购代理
            r_agent = self._agent.search(line)
            if r_agent:
                # print "%-20s\t%s" % (name_agent, r_agent.group())
                if str_agent == "":
                    str_agent = r_agent.group()

            # 提取报名时间
            r_papertm = self._papertm.search(line)
            if r_papertm:
                r_papertm2 = self._tm2.search(r_papertm.group())
                if r_papertm2:
                    # print "%-20s\t%s" % (name_papertm, r_papertm2.group())
                    if str_papertm == "":
                        str_papertm = r_papertm2.group()

            # 提取截止时间
            r_betm = self._betm.search(line)
            if r_betm:
                r_betm2 = self._betm.search(r_betm.group())
                if r_betm2:
                    # print "%-22s\t%s" % (name_betm, r_betm2.group())
                    if str_betm == "":
                        str_betm = r_betm2.group()  # inputfile = sys.argv[1]

            # 提取项目预算
            r_budget = self._budgetcheck.search(line)
            if r_budget and str_budget == "":
                r_budget = self._budget.search(line)
                if r_budget:
                    str_budget = r_budget.group()

            # 提取包类型
            r_ntype = self._ntype.search(line)
            if r_ntype and str_ntype == "":
                str_ntype = r_ntype.group()

            # 提取资质要求
            if (aptitude_flag != 2):
                ap_end = self._aptitudeend.search(line)
                if aptitude_flag == 1 and ap_end is None:
                    str_aptitude = str_aptitude + line

                ap_start = self._aptitudestart.search(line)
                if ap_start:
                    # print "资质开始－>"+ ap_start.group()
                    aptitude_flag = 1

                if ap_end:
                    # print "资质结束->" + ap_end.group()
                    aptitude_flag = 2

            # 提实施内容
            # r_actualize = self._actualize.search(line)
            # if r_actualize and str_actualize == "":
            # 	str_actualize = r_actualize.group()


            # 提取包标题
            if (actualize_flag != 2):
                stitle_cont = self._actualize_title.search(line)
                if actualize_flag == 1 and stitle_cont is not None:
                    # print "子包标题:－>" + stitle_cont.group(1)
                    str_stitle_list.append(stitle_cont.group(1))

                if actualize_flag == 1 and stitle_cont is None:
                    # print "子包提取结束:－>" + line
                    actualize_flag = 2

                stitle_start = self._actualize_tablehead.search(line)
                if stitle_start:
                    # print "子包提取开始:－>" + stitle_start.group()
                    actualize_flag = 1

        # print "%s : %s" % (self._content, title.strip('\n'))
        print "%-20s\t%s" % (name_buyer, str_buyer)
        print "%-20s\t%s" % (name_agent, str_agent)
        print "%-20s\t%s" % (name_papertm, str_papertm)
        print "%-22s\t%s" % (name_betm, str_betm)

        print "%-20s\t%s" % (name_budget, str_budget)
        print "%-20s\t%s" % (name_ntype, str_ntype)
        # print "%-20s\t%s" % (name_keylist, str_keylist)
        print "%-22s\t%s" % (name_aptitude, str_aptitude)
        print "%-22s\t%s" % (name_actualize, str_actualize)
        for title in str_stitle_list:
            print "%-22s\t%s" % (name_stitle, title)

        self.info_dict["name_buyer"] = str_buyer
        self.info_dict["name_agent"] = str_agent
        self.info_dict["name_papertm"] =  str_papertm
        self.info_dict["name_betm"] = str_betm
        self.info_dict["name_budget"] =  str_budget
        self.info_dict["name_ntype"] = str_ntype
        self.info_dict["name_aptitude"] =  str_aptitude
        self.info_dict["name_actualize"] = str_actualize
        self.info_dict["name_stitle"] =  str_stitle_list

        return self.info_dict


if __name__ == '__main__':
    content = open("344694.txt").readlines(1000)
    parser = KeyWordSearch(content)
    parser.fetchHandle()


# content = "包3 VI标识装修外的营业厅非标准 项 1.00"
# #_budget = re.compile("(?<=(预算金额)).*([1-9]\d*万元)(?=[，。])")
# _budget = re.compile("包[0-9]{0,3} (.+?) ")
# x = _budget.search(content)
# result = x.group(1)
# print "%s" % (result)

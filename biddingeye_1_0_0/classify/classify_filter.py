#!/bin/env python
# coding:utf-8
import re

focusnoticelist = [
        "传统短信", "反欺诈", "金融", "可视化", "骚扰", "态势感知",
        "脱敏", "位置服务", "物联网", "信息安全", "营销", "云计算",
        "资源池", "汽车", "大数据", "NFV", "其它"
    ]

class ClassifyMan():

    washnoticelist = [
        "维修", "机房", "租赁", "施工", "装修", "空调", "物业", "消防", "电梯", "食堂",
        "监理", "物流", "法律", "保养", "广告宣传", "终端采购", "安保", "体检", "宣传物料",
        "发电机", "电视", "绿化", "保安", "户外广告", "物资采购", "制作采购", "迎新",
        "食材", "视频会议", "外墙", "促销", "活动采购", "手机维修", "路演", "办公场所",
        "产业园", "广告牌", "家具", "搬运服务", "轮胎", "测试仪", "地板", "劳保用品",
        "绿植", "邮寄", "耗材采购", "筹办", "抱杆", "快递", "车身", "机柜", "灭火器",
        "变电所", "线路工程", "暖气", "印刷品", "灯箱广告", "报废物资", "防病毒", "大赛"
        "净化", "电源模块", "杂志", "净水", "桶装水", "铜鼻子", "车体", "责任险", "堡垒机",
        "配电室", "博览会", "展台", "修理", "网卡", "灯具", "拆闲补忙", "展示中心", "适配器",
        "供配电", "逆变器", "汽车集团", "户外大屏", "网吧", "语音通信卡", "汽车清洗"
    ]

    def noticefilter(self, textinfo):
        if self.washfilter(textinfo) == 0:
            return 0

        return 1

    #清洗分类项
    def washfilter(self, textinfo):
        if textinfo is None or len(textinfo) <= 0:
            return 0

        for keystr in self.washnoticelist:
            if keystr in textinfo:
                return 0

        return 1


    #关注分类项
    def focusfilter(self, textstr):
        if textstr is None or len(textstr) <= 0:
            return None

        focuslist = []
	str_1 = "分公司".decode("utf8")
	if str_1 in textstr:
	    return focuslist

        print "内部处理title:"+textstr
        #反馈分类表
        # egrep
        # "(短信)|(彩信)" $FILE | grep - v
        # "短信猫" > $OUTDIR
        # "/"$TYPE1
        # ".txt"
        # ====================传统短信======================
        pat1 = "短信".decode("utf8")
        pat2 = "彩信".decode("utf8")
        matchObj = re.search(r'(%s)|(%s)'%(pat1, pat2), textstr, re.M | re.I)
        if matchObj:
            if "短信猫" not in textstr:
                focuslist.append("传统短信")

        # ====================反欺诈======================
        pat1 = "欺诈".decode("utf8")
        pat2 = "诈骗".decode("utf8")
        pat3 = "伪基站".decode("utf8")
        matchObj = re.search(r'(%s)|(%s)|(%s)'%(pat1,pat2,pat3), textstr, re.M | re.I)
        if matchObj:
            focuslist.append("反欺诈")

        # ====================可视化======================
        pat1 = "可视化".decode("utf8")
        matchObj = re.search(r'(%s)'%(pat1), textstr, re.M | re.I)
        if matchObj:
            focuslist.append("可视化")

        # ====================骚扰======================
        pat1 = "骚扰".decode("utf8")
        matchObj = re.search(r'(%s)'%(pat1), textstr, re.M | re.I)
        if matchObj:
            focuslist.append("骚扰")

        # ====================NFV======================
        pat1 = "NFV"
        matchObj = re.search(r'(%s)'%(pat1), textstr, re.M | re.I)
        if matchObj:
            focuslist.append("NFV")

        # ====================态势感知======================
        pat1 = "态势".decode("utf8")
        pat2 = "舆情".decode("utf8")
        pat3 = "风险控制".decode("utf8")
        pat4 = "风控".decode("utf8")
        pat5 = "人群聚集".decode("utf8")
        pat6 = "感知".decode("utf8")

        matchObj = re.search(r'(%s)|(%s)|(%s)|(%s)|(%s)|(%s)'%(pat1,pat2,pat3,pat4,pat5,pat6), textstr, re.M | re.I)
        if matchObj:
            focuslist.append("态势感知")

        # ====================脱敏======================
        pat1 = "脱敏".decode("utf8")
        pat2 = "敏感".decode("utf8")
        pat3 = "泄密".decode("utf8")
        matchObj = re.search(r'(%s)|(%s)|(%s)'%(pat1,pat2,pat3), textstr, re.M | re.I)
        if matchObj:
            focuslist.append("脱敏")

        # ====================位置服务======================
        pat1 = "位置".decode("utf8")
        pat2 = "微网格".decode("utf8")
        pat3 = "轨迹".decode("utf8")
        matchObj = re.search(r'(%s)|(%s)|(%s)'%(pat1,pat2,pat3), textstr, re.M | re.I)
        if matchObj:
            focuslist.append("位置服务")

        # ====================信息安全======================
        if "安全" in textstr:
            pat1 = "信息安全".decode("utf8")
            pat2 = "溯源".decode("utf8")
            matchObj = re.search(r'(%s)|(%s)'%(pat1, pat2), textstr, re.M | re.I)
            if matchObj:
                focuslist.append("信息安全")

        # ====================营销======================
        pat1 = "精准".decode("utf8")
        matchObj = re.search(r'(%s)'%(pat1), textstr, re.M | re.I)
        if matchObj:
            if "营销活动" in textstr or "租赁" in textstr or "办公场所" in textstr:
                pass
            else:
                focuslist.append("营销")

        # ====================资源池======================
        pat1 = "资源池".decode("utf8")
        pat2 = "公有云".decode("utf8")
        pat3 = "私有云".decode("utf8")
        pat4 = "混合云".decode("utf8")
        pat5 = "分布式".decode("utf8")
        pat6 = "公众云".decode("utf8")
        pat7 = "公众服务云".decode("utf8")
        pat8 = "桌面云".decode("utf8")
        pat9 = "政务云".decode("utf8")
        matchObj = re.search(r'(%s)|(%s)|(%s)|(%s)|(%s)|(%s)|(%s)|(%s)|(%s)'%(pat1,pat2,pat3,pat4,pat5,pat6,pat7,pat8,pat9), textstr, re.M | re.I)
        if matchObj:
            focuslist.append("资源池")

        # ====================汽车======================
        pat1 = "汽车".decode("utf8")
        pat2 = "自动驾驶".decode("utf8")
        matchObj = re.search(r'([vV]2[xX])|(%s)|(%s)'%(pat1,pat2), textstr, re.M | re.I)
        if matchObj:
            if "汽车保险" in textstr or "汽车站" in textstr or "汽车配件" in textstr \
                    or "修理厂" in textstr or "客运站" in textstr:
                pass
            else:
                focuslist.append("汽车")

        #====================金融类筛选======================
        if "金融" in textstr:
            pat1 = "金融职业学院".decode("utf8")
            rstr1 = re.sub(r'%s'%(pat1), "", textstr)
            print(rstr1)
            pat2 = "金融商贸重点集团".decode("utf8")
            rstr2 = re.sub(r'%s'%(pat2), "", rstr1)
            print(rstr2)
            pat3 = "金融".decode("utf8")
            matchObj = re.search(r'(%s)'%(pat3), rstr2, re.M | re.I)
            if matchObj:
                if "终端" in rstr2 or "设备采购" in rstr2 or "视频监控改造" in rstr2:
                    #不符合金融分类要求
                    pass
                else:
                    # 符合金融分类要求
                    focuslist.append("金融")


        # ====================物联网类筛选======================
        if "物联网" in textstr or "车务通" in textstr:
            pat1 = "中移物联网有限公司".decode("utf8")
            rstr1 = re.sub(r'%s'%(pat1), "", textstr)
            print(rstr1)
            pat2 = "物联网公司".decode("utf8")
            rstr2 = re.sub(r'%s'%(pat2), "", rstr1)
            print(rstr2)
            pat3 = "物联网".decode("utf8")
            pat4 = "车务通".decode("utf8")
            matchObj = re.search(r'(%s)|(%s)'%(pat3, pat4), rstr2, re.M | re.I)
            if matchObj:
                if "终端" in rstr2 :
                    # 不符合金融分类要求
                    pass
                else:
                    # 符合金融分类要求
                    focuslist.append("物联网")

        # ====================云计算类筛选======================
        if "云计算" in textstr:
            pat1 = "云计算和大数据中心".decode("utf8")
            rstr1 = re.sub(r'%s'%(pat1), "", textstr)
            print(rstr1)
            pat2 = "云计算数据中心".decode("utf8")
            rstr2 = re.sub(r'%s'%(pat2), "", rstr1)
            print(rstr2)
            pat3 = "大数据产业园".decode("utf8")
            rstr3 = re.sub(r'%s'%(pat3), "", rstr2)
            print(rstr3)
            pat4 = "数据中心".decode("utf8")
            rstr4 = re.sub(r'%s'%(pat4), "", rstr3)
            print(rstr4)

            pat5 = "云计算中心".decode("utf8")
            rstr5 = re.sub(r'%s'%(pat5), "", rstr4)
            print(rstr5)
            pat6 = "云计算".decode("utf8")
            matchObj = re.search(r'(%s)'%pat6, rstr5, re.M | re.I)
            if matchObj:
                focuslist.append("云计算")

        # ====================大数据类筛选======================
        if "大数据" in textstr or "精准" in textstr or "hadoop" in textstr:
            pat1 = "大数据中心".decode("utf8")
            rstr1 = re.sub(r'%s'%(pat1), "", textstr)
            print(rstr1)
            pat2 = "大数据产业园".decode("utf8")
            rstr2 = re.sub(r'%s'%(pat2), "", rstr1)
            print(rstr2)
            pat3 = "大数据".decode("utf8")
            pat4 = "精准".decode("utf8")
            matchObj = re.search(r'(%s)|(%s)|(hadoop)'%(pat3,pat4), rstr2, re.M | re.I)
            if matchObj:
                # 符合金融分类要求
                focuslist.append("大数据")
	
        print "focuslist len:"+str(focuslist)
        for type in focuslist.__iter__():
            print(type)

        return focuslist


#测试
if __name__ == '__main__':
    #titlestr = "山东移动烟台分公司金融2017年农科院物联网及自动温控系统采购项目_中移物联网有限公司比选公告物联网公司"
    #titlestr = "中移互联网有限公司2017年工单管理平台软件开发服务项目比选公告"
    #titlestr = "中移互联网有限公司2017年MM 安全中心软件开发服务项目比选公告"
    #titlestr = "青海移动省网CMNET七期配套留存采集软件采购比选公告"
    titlestr = "2017年全省信息安全服务"
    # titlestr = "咪咕文化MiGuNet三期能力平台工程采购项目招标公告"
    # titlestr = "2016年咪咕视讯数据防泄漏项目招标公告"
    # testclass = ClassifyMan()
    # focuslist = []
    # focuslist = testclass.focusfilter(titlestr)
    # for type in focuslist.__iter__():
    #     print(type)

    matchObj = re.search(r'(信息安全)|(溯源)', titlestr, re.M | re.I)
    if matchObj:
        print "###为信息安全数据:" + titlestr


    testclass = ClassifyMan()
    print testclass.__class__
    #
    # testclass = ClassifyMan()
    # file = open("rst.txt")
    # count = 0
    # while 1:
    #     line = file.readline()
    #     if not line:
    #         break
    #
    #     linearray = line.split()
    #     if len(linearray) < 2:
    #         continue
    #
    #     if len(linearray[1]) > 0:
    #         #清洗
    #         if testclass.washfilter(linearray[1]) == 0:
    #             continue
    #         #提取
    #         focuslist = testclass.focusfilter(linearray[1])
    #         for typetitle in focuslist.__iter__():
    #             if typetitle in focusnoticelist:
    #                 filename = "test/"+typetitle+".txt"
    #                 fileobj = open(filename, 'a')
    #                 fileobj.write(linearray[1]+'\n')
    #                 fileobj.close()
    #                 count = count + 1

    # print "识别价值数据:" + str(count)






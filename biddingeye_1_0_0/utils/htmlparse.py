#encoding=utf8
from HTMLParser import HTMLParser


class PyEventParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self._tagname = "tr"
        self._p_segment = 0
        self._table_segment = 0
        self._span_segment = 0
        self._count = 0
        self._events = dict()
        self._flag = ''
        self._starttag = 'table'
        self._init = 0
        self._textbuf = ""
        self._resultbuf = ""
        #self._filename = filename

    def handle_starttag(self, tag, attrs):
        #print tag
        if tag == self._starttag and self._init == 0:
            self._init = 1
            return

        if tag == self._tagname:
            self._count += 1
            self._events[self._count] = dict()
            self._flag = self._tagname


        if tag == 'th':
            self._flag = 'th'

        if tag == 'td':
            self._flag = 'td'

        if tag == 'p':
            self._p_segment = 1

        if tag == 'table':

            for key, value in attrs:
                #key, value = dict
                if key == "border" and value == "0":
                    return

            print str(attrs)
            self._table_segment = 1
            self._textbuf ="表格X:\n"

        if tag == "div":
            self._flag = 'div'

        if tag == "span":
            """对段落文本内容进行提取操作"""
            self._span_segment = 1
            self._flag = 'span'

        #
        #if tag == 'dif' and attrs.__contains__(('class', 'event-location')):
        #    self._flag = 'event-location'

    def handle_endtag(self, tag):
        #print tag

        if tag == 'span' and self._p_segment == 0:
            self.write_tag_text(self._textbuf)
            self._textbuf = ""

        if tag == 'p':
            self._p_segment = 0
            self.write_tag_text(self._textbuf)
            self._textbuf = ""

        if tag == 'tr' and self._table_segment == 1:
            """tr 处理表格换行"""
            self.write_tag_text(self._textbuf + '\n')
            self._textbuf = ""

        if tag == 'table' and self._table_segment == 1:
            self._table_segment = 0


    def handle_data(self, data):
        # print "flag:" + str(self._flag)
        # print "data:" + data
        if self._flag == None and self._span_segment == 1:
            self._textbuf += data

        if self._flag == 'tr':
            self._events[self._count][self._flag] = data

        if self._flag == 'th':
            if self._table_segment == 1:
                self._textbuf += (data + ' ')

        if self._flag == 'td':
            if self._table_segment == 1:
                self._textbuf += (data + ' ')

        if self._flag == "td":
            self._events[self._count][self._flag] = data
        if self._flag == 'div':
            self._events[self._count][self._flag] = data
        if self._flag == 'span':
            self._events[self._count][self._flag] = data
            #print "span content:" + data
            self._textbuf += data
            #print "textbuf:" + self._textbuf


       # print data
        self._flag = None

    def write_tag_text(self, text):
        #print text
        self._resultbuf = self._resultbuf + text.strip() + '\n'
        #open(self._filename, "at").write(text.strip()+'\n')


    def event_list(self):
        #print u'近期关于Python的会议有：', self._count, '个，具体如下：'
        for event in self._events.values():
            print event
            #print event['tr-title'], '\t', event['td'], '\t', event['div'], '\t', event['span']
    def result_print(self):
        print self._resultbuf

    def get_result(self):
        return self._resultbuf


if __name__ == '__main__':
    try:
        content = open("content_demo2.txt").read()
        print content
        parser = PyEventParser()
        parser.feed(content)
        parser.result_print()
       # parser.event_list()
    except IOError,e:
        print 'IOError:', e

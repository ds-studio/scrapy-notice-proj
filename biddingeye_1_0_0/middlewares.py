# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import base64

class ProxyMiddleware(object):
	def process_request(self, request, spider):
		request.meta['proxy'] = "http://proxy.neusoft.com:8080"
		proxy_user_pass = "sun.yue:LNln618@#"
		#proxy_user_pass = "mid-smias:OP.m-i875*&n"
		encoded_user_pass = base64.b64encode(proxy_user_pass)
		request.headers['Proxy-Authorization'] = 'Basic' + encoded_user_pass

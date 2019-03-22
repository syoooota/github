# -*- coding:utf-8 -*-

import urllib.request, urllib.error


url = "http://www.nostarch.com"

headers = {}
headers['User-Agent'] = "Googlebot"

request = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(request)

print(response.read())
response.close()

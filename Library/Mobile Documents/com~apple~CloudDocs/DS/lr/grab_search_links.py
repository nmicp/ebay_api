#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 14:26:50 2021

@author: KarolinaNaranjo
"""

import urllib
import lxml.html
import ssl
import requests


ssl._create_default_https_context=ssl._create_unverified_context

url="https://www.restituciondetierras.gov.co/search?q=desistimiento"

connection=urllib.request.urlopen(url)
dom=lxml.html.fromstring(connection.read())


r= dom.xpath("//p[@class='search-total-label text-default']")[0]
res=int(r.text.split(" ")[0]) # how many links to save and iterate with 
print("The number of results is "+str(res))
print(r.text)

i=1

for p in dom.xpath("//div[@class=' autofit-col autofit-col-expand']/h4/a"): #getting the links from the search results (URT website)
    raw_url=p.attrib['href']
    print(p)
    
    print(str(i))
    #print(raw_url)
    i+=1

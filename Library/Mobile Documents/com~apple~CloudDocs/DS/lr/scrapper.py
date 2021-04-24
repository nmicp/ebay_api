#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 21:22:22 2021

@author: KarolinaNaranjo
"""
import urllib
import lxml.html
import ssl
import requests
import math

import urllib3
urllib3.disable_warnings()


query=input("Search term: ")
query=query.replace(" ","+")

#url="https://www.restituciondetierras.gov.co/search?q=desistimiento"
url="https://www.restituciondetierras.gov.co/search?q="+query
print("URL is "+url)

#connect to website
ssl._create_default_https_context=ssl._create_unverified_context
connection=urllib.request.urlopen(url)
#bring content for scrapping
dom=lxml.html.fromstring(connection.read())

r= dom.xpath("//p[@class='search-total-label text-default']")[0] #select desired dom object by class - selector
res=int(r.text.split(" ")[0]) # get total number of links found 
print("The number of results is "+str(res))
print(r.text)

delta=20 #number of entries per page -URT determined those parameters 
pages= math.ceil(res/delta)# calculates how many pages of results users get 
                            # ceil = ceiling function round up

print("the number of pages is "+str(pages))
i=1

current_page=1
pages=1

while current_page<=pages:
    connection=urllib.request.urlopen(url+"&delta="+str(delta)+"&start="+str(current_page))
    dom=lxml.html.fromstring(connection.read())
    for p in dom.xpath("//div[@class=' autofit-col autofit-col-expand']/h4/a"): #getting the links from the search results (URT website)
        raw_url=p.attrib['href']
        #print(p)
        
        print("currently processing entry No. "+str(i))
        #print(raw_url)
        i+=1
        #get pdf file from link
        entry_connection=urllib.request.urlopen(raw_url)
        entry_dom=lxml.html.fromstring(entry_connection.read())
        
        #file grabbing
        #for p in entry_dom.xpath("//img[@class=' preview-file-document  preview-file-document-fit']"):
        for p in entry_dom.xpath("//input[@id='_com_liferay_document_library_web_portlet_DLPortlet_INSTANCE_c5xZgRhOI3h9_urlInput']"):
            #pdf_raw_url=p.attrib['src']
            pdf_raw_url=p.attrib['value']
            #print(pdf_raw_url)
            #print("Original url is "+pdf_raw_url)
            pdf_url_fixed=pdf_raw_url.split('pdf')[0]+"pdf"
            #print("The pdf url is "+pdf_url_fixed)
            r= requests.get(pdf_url_fixed, stream ="True", verify=False)
            
            crop_pos=pdf_url_fixed.rfind('/')
            filename=pdf_url_fixed[crop_pos+1:]
            print("intended filename is "+filename)
            #filename="karuno2.pdf"
        
            with open (filename, "wb") as pdf:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                       pdf.write(chunk)
        
        
    # =============================================================================
    #     images=convert_from_path(filename) #covert pfd file to images (an array starts at 0)
    #     
    #     aux=filename.split("pdf")[0]
    #     
    #     for i in range(len(images)): #save the images to files
    #         images[i].save(aux+"page"+ str(i+1) +".jpg","JPEG")
    #     
    # =============================================================================
    current_page+=1
         
    
    
    
    
    
#At first God and I understood this code. Now only God knows.
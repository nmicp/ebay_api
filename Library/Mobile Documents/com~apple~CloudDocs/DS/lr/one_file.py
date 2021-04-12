#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 09:07:47 2021

@author: KarolinaNaranjo
"""

import urllib
import lxml.html
import ssl
import requests
from pdf2image import convert_from_path


ssl._create_default_https_context=ssl._create_unverified_context

url="https://www.restituciondetierras.gov.co/edictos-de-control-interno-disciplinario/-/document_library/c5xZgRhOI3h9/view_file/161728"

connection=urllib.request.urlopen(url)
dom=lxml.html.fromstring(connection.read())

for p in dom.xpath("//img[@class=' preview-file-document  preview-file-document-fit']"):

    pdf_raw_url=p.attrib['src']
    #print(pdf_raw_url)
    

print("Original url is"+pdf_raw_url)

pdf_url_fixed=pdf_raw_url.split('pdf')[0]+"pdf"

print("The pdf url is "+pdf_url_fixed)



r= requests.get(pdf_url_fixed, stream ="True", verify=False)

filename="karuno2.pdf"

with open (filename, "wb") as pdf:
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
           pdf.write(chunk)


images=convert_from_path(filename) #covert pfd file to images (an array starts at 0)

aux=filename.split("pdf")[0]

for i in range(len(images)): #save the images to files
    images[i].save(aux+"page"+ str(i+1) +".jpg","JPEG")
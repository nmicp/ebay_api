#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 08:31:14 2021

@author: KarolinaNaranjo
"""

import urllib
import lxml.html
import ssl

ssl._create_default_https_context=ssl._create_unverified_context

url="https://www.restituciondetierras.gov.co/edictos-de-control-interno-disciplinario/-/document_library/c5xZgRhOI3h9/view_file/161728"

connection=urllib.request.urlopen(url)
dom=lxml.html.fromstring(connection.read())

#for p in dom.xpath('//img/@src'):
for p in dom.xpath("//img[@class=' preview-file-document  preview-file-document-fit']"):
    print(p.attrib['src'])
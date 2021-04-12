#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 13:55:23 2021

@author: KarolinaNaranjo
"""

import requests
from pdf2image import convert_from_path



#pdf_url="https://www.restituciondetierras.gov.co/documents/20124/158679/RC+01409+decide+desistimiento+(1).pdf"

pdf_url="https://www.restituciondetierras.gov.co/documents/20124/158679/RC+01357+decide+desistimiento+%281%29.pdf/e7d0fe28-1c3f-1388-9322-8cd3fb8ae5a8?version=1.1&t=1576612690945&previewFileIndex=1"
print("Original url is"+pdf_url)

pdf_url_fixed=pdf_url.split('pdf')[0]+"pdf"

print("The pdf url is "+pdf_url_fixed)



# r= requests.get(pdf_url, stream ="True", verify=False)

# with open ("karuno.pdf", "wb") as pdf:
#     for chunk in r.iter_content(chunk_size=1024):
#         if chunk:
#            pdf.write(chunk)


# images=convert_from_path("karuno.pdf") #covert pfd file to images (an array starts at 0)

# for i in range(len(images)): #save the images to files
#     images[i].save("page"+ str(i+1) +".jpg","JPEG")
    

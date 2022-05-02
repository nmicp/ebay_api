#!/usr/bin/env python
# coding: utf-8

# ## **Appendix C** 
# 
# 
# This file should help navigate the folders in the "nmicp" project space on Rivanna
# 
# ## Types of File Extensions
# 
# ### .ipynb
# This file type is a notebook file for python. This allows you to run code and to markdown the page to make comments and structure. 
# 
#    - To run each cell click "SHIFT ENTER" or press the play button (arrow pointing to the right) on the top bar. 
# 
#    - "#" in python are comments. You can use "#" to comment out lines of code or to make remarks.
# 
# ### .csv
# A delimited text file separated by commas by default (comma seperated values). You can download these files to upload to whatever software you are using. Data from this project can be downloaded as a csv file either through AccessingData.ipynb or through the datasette module.
# 
# ### .py
# Programming file for python. This can be written in a text editor, and allows all the code in the script to run at once. Our main script for data collection, and our script for category lists exist as this type of file. 
# 
# ### .out
# This file type stores executable code. This is automatically generated from the slurm script, and can stores information if any errors occur. You should not have to edit this directly. 
# 
# ### .slurm
# This file type is where we include parameters of running the automated script. More information of specific parameters are included in the metadata documentation. 
# 
# ### .db
# The database that is being updated everynight when new data ia collected. You will not be able to click and open this file, but instead access it contents through the datasette module (instructions in book) or through code.
# 
# ---
# ## Files
# 
# 
# ### navigation.ipynb
# This file should contain a high level overview of what each file contains.
# 
# ### categories_capstone.csv
# A csv file of the categories and category ids of the original data pipeline constructed by the NMICP capstone team.
# 
# ### CategoryList_Input.py
# Python script of categories in data collection process. This file can be edited to include/remove category ids from eBay. eBay category IDs can be found <a href="https://pages.ebay.com/sellerinformation/news/fallupdate16/category-and-item.html">here</a>.
#  
# You can select specific categories to see a full list of category IDs. 
# 
# The main python script (eBay_datacollection.py) is written in a way that collects data that maximizes the number of observations. If you **add** a category ID, it should not affect the data pipeline and collection. A maximum number of category IDs in this list should be 50. 
# 
# ### eBay_datacollection.py
# This is the main script that contains the code to collect data from eBay. This script is well-commented and includes information on what certain code blocks do. 
# 
# ### keys.env
# This file type stores your keys privately. These keys were obtained through eBay's developer's program. The keys were then used in the main python file to connect and collect data.
# 
# ### eBay_Slurm.slurm
# The file where we include parameters of running the automated script. 
# 
# ### result.out
# Should print “Submitted batch job [number]" when automated job is submitted correctly. 
# 
# ### log.out
# Created when something goes wrong. It will specify the error from the main script. 
# 
# ### eBay.db 
# The database that contains the data. Data can be accessed from Accessingdata or through datasette. 
# 
# ### Accessingdata.ipynb 
# This file serves as another way to access and download the data in csv form. 
# 
# ### ebay_data_4_27.csv
# Data collected from UVA Capstone team before automation is restarted in this nmicp space. Data is collected until 4-26-2022. 

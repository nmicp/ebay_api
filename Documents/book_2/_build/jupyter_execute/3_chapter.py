#!/usr/bin/env python
# coding: utf-8

# ## **Getting Data from eBay** 
# 
# ### **Introduction to the eBay Data Pipeline**
# 
# In this chapter, we will provide a detailed overview of the implementation of a data pipeline. This process begins by collecting keys from eBay’s Developer Program, and ends in a cleaned data frame that is connected to a SQLite database.  Figure 3 provides a holistic overview of our data pipeline process. Orange elements within the inner rectangle are applied to each category in our predefined <code>categories_list</code>. The looping structure of the flowchart represents the automated nature of this entire process, which runs once every 24 hours. We start by loading in the developer keys provided by eBay and connecting to their API system. Developer’s keys are a username and password that is unique to each user of eBay’s developer’s program. These keys are unique to each user and act as identifiers for users when accessing the API systems. The purpose of this is for eBay to keep track of who is accessing what at any given time, and as such, developer keys should be stored in a hidden .env file as a prerequisite of the loading process. Using .env files is a customary method for storing private information, and often reside in the same directory as the main code files. It is important to not share your keys with anyone!
#  
# Once we gain access to eBay’s API system, we define the <code>geteBay</code> function. This function intakes a category number as an input, and subsequently connects to and makes GET request calls to the Finding API. This function must be defined before the iterative process described below can be completed. Specifics on how this function works will be provided in future chapters. 
#  
# Once the  <code>geteBay</code> function  has been defined, we iteratively loop over each of the categories in <code>categories_list</code>, and each element is passed through the <code>geteBay</code> function. The <code>geteBay</code> function contains loops that extracts each of the desired features and cleans the associated data for each listing. The cleaned data is then stored in a new data frame.
#  
# After the cleaned data frame is generated, we extract the <code>Item_ID</code> for each listing and use the resulting list as an input parameter to our second API connection with the Shopping API. The subsequent GET request calls allows us to mine further features of interest for each of the listings:
# 
# - <code>category_id</code>
# - <code>item_specs</code>
# - <code>item_idlist</code>
# - <code>seller_id</code>
# - <code>Item_sku</code> 
# - <code>image_url</code>
# 
# Next, we merge the processed data from the Finding and Shopping APIs into a single data frame called <code>item_specs</code>.
#  
# We then connect to our SQL database, ebay.db, and listings in the newly merged <code>item_specs</code> data frame are appended to the item_specs table. Once the new data has successfully been appended to the database table, all changes are saved and the connection to the database is closed. This process then repeats the following day at 12.05am.
# 
# *figure 3.* The automated data collection process. This flowchart represents the overall automated data collection process that we built. The inner box indicates a comprehensive process to collect for each category. Then, the data is concatenated and the collection process is automated each 24 hours. 
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/fig7.jpg" width=500 height=700 />
# 
# 

# ### **Flask App** <a class="anchor" id="section_3_2_1"></a>
# 
# **Building a Simple App**
# 
# Getting access to eBay’s developer’s program requires users to build their own application. This requirement is a result of eBay’s marketplace account <a href="https://developer.ebay.com/marketplace-account-deletion"> deletion notification update </a>. The resulting application provides eBay with a communication channel to notify developers of marketplace deletion notifications. The architecture the application requires is relatively simple – it needs to receive eBay challenge code and respond with an output that hashes together the challenge code, the user’s eBay verification token, and the application’s endpoint. A 200 response should be produced in an output field in JSON format. An application that meets these requirements can be constructed in python using the flask package.
# 
# It should be reiterated that creating an application that can successfully receive challenge code is essential to accessing eBay’s production data. Production data consists of real listings from live marketplaces. Users can also develop test code to interact with eBay’s API system through their Sandbox environment.
# 
# ```python
# 
# from flask import Flask, jsonify, Request, Response, request
# import hashlib
# 
# app = Flask(__name__)
# 
# @app.route('/', methods=['GET', 'POST'])
# def hello_world():
#     if request.method == "POST":
#         request_data = request.get_json()
#         return Response(status=200)
# 
#     challengeCode = request.args['challenge_code']
#     endpoint = 'https://ncimpcapstone.club'
#     verificationToken = 'username'
#     m = hashlib.sha256(str(str(challengeCode)+verificationToken+endpoint).encode('utf-8'))
#     myDict = {'challengeResponse':m.hexdigest()}
#     return jsonify(myDict)
# 
# if __name__ == "__main__":
#     app.run(host='0.0.0.0')
# 
# ```
# 
# The Flask application must be able to manage Hyper Text Transfer Protocol Secure (HTTPS) requests. HTTPS is the secure version of HTTP, the protocol over which data is sent between two applications. The method we used to get an https connection was through letsencrypt.com, which is a third-party website that provides a certificate to most hosted websites. The user needs to purchase a domain name in order to obtain an SSL certificate. Domains can be purchased through godaddy, Google domains, or other websites. There is no restriction on extensions. For example, we used a .club extension due to its low set up cost. After securing an SSL hosted domain for the application, login to eBay’s developer’s program and apply for Production Keys. Once Production Keys are obtained, you are ready to start building your data pipeline.
# 
# For help on troubleshooting setting up a Flask app, look into UVA IT and various online resources including  <a href="https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-20-04">this tutorial</a>. The flask package also has documentation that can be accessed at <a href="https://flask.palletsprojects.com/en/2.0.x/">this link</a>.
# 

# ## **Navigating through the Code** 
# 
# This section contains information on our specific implementation of a data pipeline that extracts data from eBay, cleans the data, and uploads it to a database. The script was written in Python, and lives on a high performance computing system (Rivanna). Access to the script and the computing system was established before the project was handed off to stakeholders. Python is a high-level, general-purpose programming language. The specific structure of Python is similar to R in that it includes variable names and functions built into the language. In this python script, we go through a detailed description of the code we implement. This is a specific use-case of the data pipeline that extracts data from the predefined categories of interest we defined earlier. To troubleshoot Python errors, Google and StackOverflow — a question and answer website for programming — can be helpful. 
# 
# This section is meant to provide a general overview of the code in our main data mining and processing script. To help reinforce user understanding, we have included images of code blocks, which we reference throughout this tutorial. In our code blocks, we also include comments on where one can edit variables for different use-cases of our data pipeline.
# 
# As with any python script, we will begin by importing the necessary packages and loading the API keys into our environment. Packages are replicable actions that take place in Python. These are open-source, and their documentation on how to implement specific packages can be researched online. In the code that imports the packages that we use in our script, we also import a separate python script that contains our categories of interest. Notice that <code>categories_of_interest</code> is imported from another .py file, <code>CategoryList_Input</code>. This file resides in the same directory as our main .py file, and provides a method for our sponsors to freely modify categories of interest without interfacing with the main script. If you want to change the categories, simply open the <code>CategoryList_Input</code> python file, and change the category ids to those you want to search over. Throughout the script, we will directly reference where some specific packages are. 
# 
# With our implementation of this Python script, blue colored code are functions that are built into packages. Red colored code represents strings, and green code represents built in python functions not from specific packages. It is best practice to not name new variables anything that appears in green or blue, as that might overwrite the default system. 
# 
# One of the first steps is to call the modules that allows us to run the code:
# 
# 
# ```python
# 
# ## NMICP Data Engineering Pipeline
# 
# #Import necessary packages 
# import pandas as pd
# import numpy as np
# import os
# import requests
# import dotenv
# import json
# import base64
# from matplotlib import pyplot as plt
# import seaborn as sns
# from datetime import datetime, date, timedelta
# import xmltodict
# from collections import OrderedDict
# import hashlib
# import traceback
# 
# import sqlite3
# import os
# import time 
# 
# ```
# 
# After loading in our account-specific keys, an initial connection is made to the eBay API system. This establishes a general connection to eBay’s APIs. When accessing specific APIs to extract features of interest, we will have to establish other connections.  This general connection to eBay allows us to have a secure flow of data, while eBay can also keep track of the details on who is using their data. This initial setup includes getting the private keys connected to the script. These private keys are stored in a text file in the same folder that the script exists in. Other variables created including <code>url</code>, <code>headers</code>, and <code>params</code> are used to specify our connection to eBay. The <code>request.post()</code> function is the final step in creating the secure request to connect to eBay’s API. 
# 
# ```python
# 
# #Import categories list, make sure file is in same directory
# from CategoryList_Input import categories_of_interest
# 
# #Set up API Connection 
# 
# #Load secret file that contains API keys
# dotenv.load_dotenv('keys.env')
# 
# #Load in secret keys 
# AppID = os.getenv('AppID')
# DevID = os.getenv('DevID')
# CertID = os.getenv('CertID')
# 
# #Combine AppID and CertID to create encoded authorization token
# s = AppID + ':' +CertID
# encoded = base64.b64encode(s.encode('UTF-8'))
# 
# #URL that verifies API user
# url = 'https://api.ebay.com/identity/v1/oauth2/token'
# 
# #Parameters passed to the API connection
# headers = {'Authorization': 'Basic ' + str(encoded.decode("utf-8")),
#           'Content-Type': 'application/x-www-form-urlencoded'}
# 
# #Connect to API
# params = {'grant_type':'client_credentials',
#          'scope': 'https://api.ebay.com/oauth/api_scope'}
# 
# r = requests.post(url, headers=headers, params=params)
# r
# 
# 
# ```
# 
# We also define a datetime object to collect data from a timeframe of interest. For our project, we want to collect data from the last 24 hours, so the datetime function sets a timeframe for the previous day. 
# 
# 
# ```python
# #Retrieve OAuth token for connecting to the Shopping API later
# OAuth = json.loads(r.text)['access_token']
# oneday = pd.to_datetime(date.today() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
# 
# ```
# 
# Next, we dive into the overall architecture of the data pipeline. The architecture of our extraction and processing pipeline is encapsulated in a try block. We implement a try-except block in case the pipeline runs into any errors. At the end of this script, we discuss what the except blocks we implement catch. The try block runs the code, and execution only jumps to the except block if there are any errors.
# 
# We collect the corresponding data through a function we defined as <code>geteBay</code>. This function uses the Finding API to collect our initial set of features discussed in our data description. The automated nature of our data collection also stems from this section as we collect data from the past day of listings. The <code>geteBay</code> function parses through a list of predefined categories. This function also takes a <code>starttime</code> parameter that specifies the earliest time to collect listings from.
#  
# The user-defined url and headers variables are used to authenticate the connection to the Finding API and its <code>findItemsByCategory</code> function. We also initialize <code>categorydf</code> dataframe that will append data to <code>item</code>. Next, we create a <code>params</code> object that defines the output of the API call. This includes the category ID,  entries per page, number of pages, and listing time. Finally, we call the API with the constructed parameters.
# 
# 
# ```python
# 
# #--- BEGIN TRY BLOCK
# try:
# 
#     #Function to connect to eBay's Finding API and collect item listings for the given category
#     def geteBay(categoryid, starttime):
# 
#         url = 'https://svcs.ebay.com/services/search/FindingService/v1' #URL that links to the Finding API
#         headers = {'X-EBAY-SOA-SECURITY-APPNAME': AppID, #AppID is a global variable in the main script
#                    'X-EBAY-SOA-OPERATION-NAME': 'findItemsByCategory'}
#         
#         #Initialize empty dataframe
#         categorydf = pd.DataFrame()
#         
#         #Parse through desired numbers of pages in the Finding API (Given Call limits we have limited this to 2 pages)
#         for i in range(1,2):
#             #Specify API call details
#             params = {'categoryId': categoryid,
#                      'RESPONSE-DATA-FORMAT':'JSON',
#                      'paginationInput.entriesPerPage':100,  #100 entries per page. This is the maximum number of entries we can get for any one category
#                      'paginationInput.pageNumber':i,
#                      'findItemsByCategoryRequest.sortOrder':'StartTimeNewest',
#                       'itemFilter(0).name': 'StartTimeFrom',
#                       'itemFilter(0).value': starttime}
#             
#             #Make GET request call to Finding API
#             r = requests.get(url, headers=headers, params=params)
#             
# ```
# 
# If the call to the API returns empty, the for loop will skip over the page of listings it is currently iterating over without throwing an error. Data collected from the API call is then converted to tabular format and appended to a dataframe. 
# 
# 
# ```python
# 
#  #Continue to next page if nothing was collected
#             if 'item' not in pd.json_normalize(json.loads(r.text)['findItemsByCategoryResponse'][0]['searchResult'][0]):
#                 continue 
#                 
#             #Add item listings to dataframe from current page
#             categorydf = categorydf.append(pd.json_normalize(json.loads(r.text)['findItemsByCategoryResponse'][0]['searchResult'][0]['item']))
#         
#         #Reset the row index in the item dataframe
#         categorydf = categorydf.reset_index()
# 
# 
# ```
# 
# The data contained within the <code>categorydf</code> table is not uniform and still needs to be processed. To tackle this issue, we implement the following algorithmic method for each feature: initialize an empty list, iterate over the length of the dataframe, verify that the feature exists, extract key elements of the uncleaned data, and append processed results to the empty list. These steps will clean each feature of interest that is implemented in our final cleaned dataframe. Each of the lists will later be combined into a cleaned dataframe. If a row has a missing value, we assign <code>nan</code>  in string format to indicate this. This is to ensure that all features have a consistent data type and number of elements
# 
# 
# ```python
#        #Iterate through each listing of the dataframe and clean corresponding column values
#         #item ID
#         itemlist = []
#         for i in range(0, len(categorydf)): #loop over range of categorydf
#             if 'itemId' in categorydf: #if current row has an associated itemId...
#                 item = categorydf.itemId[i][0] #extract itemId...
#             else:
#                 item = 'nan' #else label as nan
#             itemlist.append(item) 
# 
#         #title
#         titlelist = []
#         for i in range(0, len(categorydf)):
#             if 'title' in categorydf:
#                 title = categorydf.title[i][0]
#             else: 
#                 title = 'nan'
#             titlelist.append(title)
# 
#         #view item url, this is NOT the image URL, it is the link to the actual listing
#         urllist = []
#         for i in range(0, len(categorydf)):
#             if 'viewItemURL' in categorydf:
#                 url = categorydf.viewItemURL[i][0]
#             else: 
#                 url = 'nan'
#             urllist.append(url)
# 
#         #postal code
#         postallist = []
#         for i in range(0, len(categorydf)):
#             if 'postalCode' in categorydf:
#                  code = categorydf.postalCode[i]
#             else:
#                  code = 'nan'
#             postallist.append(code)
# 
#         postal = []
#         for i in postallist:
#             if type(i) == list:
#                 postal.append(i[0])
#             else:
#                 postal.append("nan")
# 
# 
#         #country
#         countrylist = []
#         for i in range(0, len(categorydf)):
#             if 'country' in categorydf:
#                 a = categorydf['country'][i][0]
#             #print(a)
#             else:
#                 a = 'nan'
#             countrylist.append(a)
# 
#         #selling price
#         pricelist = []
#         for i in range(0, len(categorydf)):
#             if 'sellingStatus' in categorydf:
#                 price = categorydf.sellingStatus[i][0]['convertedCurrentPrice'][0]['__value__']
#             else:
#                 price = 'nan'
#             pricelist.append(price)
# 
#         #condition
#         conditionlist = []
#         for i in range(0, len(categorydf)):
#             if 'condition' in categorydf:
#                 a = categorydf['condition'][i]
#             else: 
#                 a = 'nan'
#             conditionlist.append(a)
# 
#         #listing time
#         listingtime = []
#         for i in range(0, len(categorydf)):
#             if 'listingInfo' in categorydf:
#                 a = categorydf['listingInfo'][i][0]['startTime'][0]
#             else:
#                 a = 'nan'
#             listingtime.append(a)
# 
#         #create final version of dataframe from cleaned item listings
#         categorydf_clean = pd.DataFrame({'Item_ID': itemlist,
#                                          'Product_Title':titlelist,
#                                          'URL_image':urllist,
#                                          'Country':countrylist,
#                                          'Price_USD':pricelist,
#                                          'Postal_Code': postal,
#                                          'Item_Condition':
#                                          conditionlist,
#                                          'Listing_Time':listingtime})
# 
#         return categorydf_clean
# 
# ```
# 
# Extracting the postal code for each listing presents a special case for the methodology described in the previous paragraph. Specifically, the output of <code>postallist</code> contains a mix of sub lists and placeholders for empty values. Heterogeneous data types are an issue, so we implement an additional processing step – if the data type of the extracted element is a list, we take the first element. This corresponds to the desired postal code value. Otherwise, we replace the placeholder value with “nan” in string format.
# 
# ```python
# 
#    #postal code
#         postallist = []
#         for i in range(0, len(categorydf)):
#             if 'postalCode' in categorydf:
#                  code = categorydf.postalCode[i]
#             else:
#                  code = 'nan'
#             postallist.append(code)
# 
#         postal = []
#         for i in postallist:
#             if type(i) == list:
#                 postal.append(i[0])
#             else:
#                 postal.append("nan")
# ```
# 
# After processing all features of interest, we create <code>categorydf_clean</code> data frame from a dictionary of lists. This data frame contains the processed data for each feature. The function outputs the cleaned dataframe. 
# 
# ```python
# 
#   #create final version of dataframe from cleaned item listings
#         categorydf_clean = pd.DataFrame({'Item_ID': itemlist,
#                                          'Product_Title':titlelist,
#                                          'URL_image':urllist,
#                                          'Country':countrylist,
#                                          'Price_USD':pricelist,
#                                          'Postal_Code': postal,
#                                          'Item_Condition':
#                                          conditionlist,
#                                          'Listing_Time':listingtime})
# 
# 
# ```
# 
# The <a href=" https://stackoverflow.com/questions/56494304/how-can-i-do-to-convert-ordereddict-to-dict "><code>OrderedDict_to_dict()</code> </a>  function is defined to help change the data type for inputs that happened to be an ordered dictionary. Converting an ordered dictionary to a dictionary allows us to parse through data in the same method discussed above. 
# 
# ```python
# 
#    def OrderedDict_to_dict(arg):
#         if isinstance(arg, (tuple, list)): 
#             return [OrderedDict_to_dict(item) for item in arg]
# 
#         if isinstance(arg, OrderedDict): 
#             arg = dict(arg)
# 
#         if isinstance(arg, dict): 
#             for key, value in arg.items():
#                 arg[key] = OrderedDict_to_dict(value)
# 
#         return arg
#     
#     #Assign categories of interest to categories_list object
#     categories_list = categories_of_interest
# 
# ```
# 
# This code block changes the directory of the collected data to the location of the database subdirectory and connects to it, using the SQLite library 
# 
# ```python
# 
#     #Change to project directory and connect to ebay.db database
#     os.chdir('/gpfs/gpfs0/project/sdscap-kropko/sdscap-kropko-network')
#     ebay_db = sqlite3.connect("ebay.db")
# 
# ```
# 
# Here we loop through the list of categories. It starts by calling the <code>geteBay</code> function and passing the current category. This will collect the results from the last 24 hours and save them to a dataframe, <code>finding_df</code>.
#  
# We also initialize an empty list and loop through the <code>finding_df</code> to extract the item IDs. 
# 
# 
# ```python
# 
#  #Loop through categories of interest
#     for cat in categories_list:
#         #Initialize item listing dataframe using our geteBay function
#         finding_df = geteBay(cat, oneday)
#         #Extract item IDs from dataframe to use in Shopping API call
#         itemlist = []
#         for i in range(0, len(finding_df['Item_ID'])):
#             item = finding_df['Item_ID'][i]
#             itemlist.append(item)
# 
# ```
# 
# We create a <code>new_list</code> that segments elements in the item ID list into groups of 20. Generating a list of lists in this format allows us to maximize the number of possible calls  we can make to the Shopping API - in this case, it’s 5,000 API calls per day.  Next, we set up the parameters to connect to the Shopping API and initialize an empty data frame; this process mirrors connecting to the Finding API.
#  
#  
# ```python
#         #Section itemlist into sets of 20 item IDs to adhere to API call limit
#         new_list = [itemlist[i:i + 20] for i in range(0, len(itemlist), 20)]
# ```
# 
# In a <code>for loop</code> we iterate through each sublist in  <code>new_list</code> and reduce the sub list’s elements into one string that contains all of the listing IDs. We pass this string to the <code>GetMultipleItems</code> and explicitly state that we want features from the following call-specific output fields: <code>Variations, Details, ItemSpecifics</code>.
# 
# We complete the call to the API and convert XML output into a dictionary, and save it in a dataframe. 
#  
# ```python
# 
# #Section itemlist into sets of 20 item IDs to adhere to API call limit
#         new_list = [itemlist[i:i + 20] for i in range(0, len(itemlist), 20)]
#        
#         #Create Shopping API call parameters
#         root = 'https://open.api.ebay.com'
#         endpoint = '/shopping'
#         headers = {'X-EBAY-API-IAF-TOKEN': 'Bearer ' + OAuth,
#                   'Content-Type': 'application/x-www-form-urlencoded',
#                   'Version': '1199'}
# 
#         #Initialize empty dataframe for Shopping API results
#         getmultipledf = pd.DataFrame()
#         
#         #Parse through sets of ItemIDs and add item information to dataframe
#         for eachlist in new_list:
#             string_listingids = ','.join(eachlist)
#             params = {'callname':'GetMultipleItems',
#                     'ItemID': string_listingids,
#                     'IncludeSelector':'Variations,Details,ItemSpecifics'}
#             
#             #Make GET request call to Shopping API
#             r = requests.get(root+endpoint, headers=headers, params=params)
#             xml_format = xmltodict.parse(r.text)
#             
#             #Append item information to dataframe
#             getmultipledf = getmultipledf.append(pd.json_normalize(OrderedDict_to_dict(xml_format)))
# 
# ```
# 
# For each iteration, we check to see if <code>GetMultipleItemsResponse.Item</code> is a valid feature in <code>getmultipledf</code>. If the feature does not exist, we skip that iteration and continue the for-loop. Then, we initialize empty lists for features of items collected by the Shopping API. All variables of interest are stored in the single column <code> GetMultipleItemsResponse.Item</code >, so we make a copy of this feature and assign it to <code>convert_list</code>. We then convert any instances of float values in <code>convert_list</code> into lists. This is a necessary processing step because we are going to iterate across the length of convert_list, and len() cannot be applied to objects with a float data type. 
# 
# 
# ```python
# 
#      #Reset row index of dataframe   
#         getmultipledf = getmultipledf.reset_index()
#         
#         #If no new items were found for current category, continue to the next one
#         if 'GetMultipleItemsResponse.Item' not in getmultipledf:
#             continue 
# ```
# 
# Once every float instance has successfully been converted to a list, <code>convert_list</code> is handed off to another recursive loop that will extract additional item-related features. Each of these values is saved to the corresponding lists:
# 
# - item_specs
# - item_idlist
# - seller_id
# - item_sku
# - image_url
# - category_id
# 
# 
# ```python
# 
#         #Initialize empty lists for item listing features
#         item_specs = []
#         item_idlist = []
#         seller_id = []
#         item_sku = []
#         image_url = []
#         category_id = []
#         
#         #Subset into dataframe section that contains item information
#         convert_list = getmultipledf['GetMultipleItemsResponse.Item']
#         
#         #Check that the object is a list, otherwise cast it into one
#         convert_list = [convert_list] if isinstance(convert_list, float) else convert_list
#         
#         #Iterate through item pages
#         for j in range(0, len(convert_list)): 
#             
#             #Continue to next iteration if out of items (ie element is empty)
#             if type(convert_list[j]) == float:
#                 continue
#             
#             #Append item information to corresponding list
#             #category ID
#             for i in range(0, len(convert_list[j])):
#                 a = getmultipledf['GetMultipleItemsResponse.Item'][j][i]['PrimaryCategoryID'] 
#                 category_id.append(a)
#             
#             #item specifics
#             for i in range(0, len(convert_list[j])):
#                 a = getmultipledf['GetMultipleItemsResponse.Item'][j][i]['ItemSpecifics']['NameValueList']
#                 item_specs.append(a)
# 
#             #item ID
#             for i in range(0, len(convert_list[j])):
#                 a = getmultipledf['GetMultipleItemsResponse.Item'][j][i]['ItemID']
#                 item_idlist.append(a)
# 
#             #seller ID (encrypted)
#             for i in range(0, len(convert_list[j])):
#                 a = getmultipledf['GetMultipleItemsResponse.Item'][j][i]['Seller']['UserID']
#                 m = hashlib.sha256(a.encode('utf8'));
#                 seller_id.append(m.hexdigest())
#                 
#             #item SKU
#             for i in range(0, len(convert_list[j])):
#                 a  = getmultipledf['GetMultipleItemsResponse.Item'][j][i].get('SKU')
#                 item_sku.append(a)
# 
#             #image URL 
#             all_picture_urls = []
#             for i in range(0, len(convert_list[j])):
#                 if isinstance(getmultipledf['GetMultipleItemsResponse.Item'][j][i]['PictureURL'], list):
#                     all_picture_urls.append(getmultipledf['GetMultipleItemsResponse.Item'][j][i]['PictureURL'])
#                 else:
#                     converted_to_list = [getmultipledf['GetMultipleItemsResponse.Item'][j][i]['PictureURL']]
#                     all_picture_urls.append(converted_to_list)
# 
#             for i in range(0, len(all_picture_urls)):
#                 a = all_picture_urls[i][0]
#                 image_url.append(a)
#         
# ```
# We combine the two cleaned data frames generated from making calls to the Finding and Shopping APIs.  Moreover, we convert the data type of  <code>Item_Condition</code>,<code>Listing_Time</code>, and <code>itemspeclist</code> to strings in order to save these columns and their corresponding values to our SQLite database. SQLite databases cannot handle datetime data types and dictionaries within a specific cell.  this final dataframe includes all the features discussed in the data description section.
# 
# ```python
#           
#         
#         #Create dataframe from Shopping API data
#         shopping_df = pd.DataFrame({'itemspeclist': item_specs,
#                                'itemid': item_idlist,
#                                'sellerid':seller_id,
#                               'sku':item_sku,
#                               'image_url':image_url,
#                                    'categoryid': category_id})
#         
#         #Combine Finding and Shopping API data in one dataframe
#         item_specs = pd.DataFrame({'ItemID':finding_df['Item_ID'],
#                                   'Product_Title':finding_df['Product_Title'],
#                                   'CategoryID':shopping_df['categoryid'],
#                                   'Price':finding_df['Price_USD'],
#                                   'Item_Condition': finding_df['Item_Condition'].astype('str'),
#                                   'Listing_Time':finding_df['Listing_Time'].astype('str'),
#                                   'Item_Specifics':shopping_df['itemspeclist'].astype('str'),
#                                   'Seller_ID':shopping_df['sellerid'],
#                                   'Country':finding_df['Country'],
#                                   'Zip_Code':finding_df['Postal_Code'],
#                                   'Image_URL':shopping_df['image_url'],
#                                   'SKU':shopping_df['sku']})
# ```
# 
# Next, after we have the cleaned dataframe containing our data of interest, we upload the new data into our SQL database. A database is an easy way to store, update, and access data. In this code block, we add the current data to the SQLite database, commit the changes, and close the connection. Our database only has a main table, so accessing the data will be easy. Accessing this database can be done with a high-level dashboard we created. Information on how to access the data can be found in the **“Accessing Data with Datasette”** section. 
# 
# 
# ```python
# 
#        #Append rows from combined dataframe to SQL database
#         item_specs.to_sql("item_specs", ebay_db, index=False, chunksize=1000, if_exists="append")
#       
#     #Commit changes to database and close connection
#     ebay_db.commit()
#     ebay_db.close()
#     
# #--- END TRY BLOCK
# 
# ```
# 
# These are the except blocks that we implement to account for any errors in our script. The first except block catches any instance of a connection error. The second block is a catch-all for any other errors our script may generate. The code block will generate a log file that stores the name of the error, the traceback message and the current category ID iteration that caused the error. Finally, as a fail-safe, we commit and close the database in these blocks, so any successfully cleaned rows prior to the error are saved. The files that output the errors exist in the same folder where we run the script. The file is titled “Ebay_Script_Log.txt”. (
# 
# These are the except blocks that we implement to account for any errors in our script. The first except block catches any instance of a connection error. The second block is a catch-all for any other errors our script may generate. The code block will generate a log file that stores the name of the error, the traceback message and the current category ID iteration that caused the error. Finally, as a fail-safe, we commit and close the database in these blocks, so any successfully cleaned rows prior to the error are saved.
# 
# 
# ```python
# 
# #--- BEGIN EXCEPT BLOCK 
# #If there is a ConnectionError at any point, skip TRY block and execute next two lines
# except ConnectionError:
#     print("A connection error occurred!")
#     
# #If there is an error besides a ConnectionError at any point, skip TRY block and execute following code
# except Exception as e:
#     categoryerror = item_specs.CategoryID.iloc[-1] #Extract most recent CategoryID that was sucessfully captured
#     
#     #Create a log file that contains error details
#     with open('Ebay_Script_Log.txt', 'w') as f: #w will overwrite existing content in the log.txt file
#         f.write(str(e)) #Add error name
#         f.write(traceback.format_exc()) #Add the error's entire traceback message
#         f.close() #Close log file
#     print("Something other than a ConnectionError happened")
#     print("Error occured at category " + str(categoryerror))
#     
#     #Commit changes to database and close connection (this will ensure all previously extracted listings are properly saved)
#     ebay_db.commit()
#     ebay_db.close()
#     
# #--- END EXCEPT BLOCK 
# 
# ```

# ### **Slurm File** 
# 
# We use a batch script to automate the data collection process. The term script is used throughout this section to mean an executable file that you create and submit to a job scheduler. In essence, this script is an automated system that will run the data collection process at a user specified time. Sbatch submits a batch script to Slurm and allows us to recursively run our main pythonic script to collect data. This slurm file should have the extension slurm_file_name.slurm. Setting up the slurm file to run on a daily basis requires several parameters listed below. These commands tell the job scheduler what to do. These options and their use cases can be added to the body of the slurm file in order to customize its functionality. The specific implementation of this slurm file to collect data from eBay everyday at midnight can be seen in the code chunk below. We choose certain parameters that will work well with eBay’s call limits. 
# 
# <code>#SBATCH --begin=00:05</code>
# The --begin parameter sets the start time you want the job to run. In this example, this initiates the job at 12.05am 
# 
# 
# <code>BATCH --output=result.out</code>
# This is the file you specify in which to store the job output.
# 
# <code>#SBATCH -p standard</code>
# This parameter specifies the partition/queue in which to run the job.
# 
# <code>#SBATCH -A "<account>"</code>
#     
# Since we are running this slurm job on a high performance computing system, this specifies the account to be charged when submitting the job. 
#     
# <code>#SBATCH -t 03:00:00</code>    
# The -t parameter sets the time limit for which the job will stop running. For this wall clock time limit, the job will run for a maximum of 3 hours. 
#     
# <code>#SBATCH --mail-type=fail</code>
# This parameter notifies the associated mail-user by email when a failed event type occurs.
#     
# <code>#SBATCH --mail-user= <user "email address"></code>
# This specifies the user’s associated email address to be notified when a failed event type occurs.
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/fig8.jpg" width=500 height=480 />
#     
# 
#     
# Once the parameters of the slurm file are set, the next step is to set up the job to run. To set this up, navigate to the folder/directory that contains the slurm script. This can be accomplished by opening a terminal (via file > new > terminal on Rivanna) and checking to see if the <code>pwd</code> (present working directory) matches the location of interest. To navigate to the correct directory use type in cd followed by the location of interest. Once you have confirmed that you are in the correct directory, type the function “sbatch slurm_file_name.slurm”. Hit enter, and if successful, the following message should appear “submitted batch job [number]”. 
# 
# There are several terminal commands that can check the status of a slurm job. These commands, and their exact syntax, are listed below:
# 
# <code>scontrol show [job number]</code>
# - Lists detailed information for a job (useful for troubleshooting)
# - The job number will change every 24 hours 
#     
# <code>squeue –start</code> List all current jobs
#     
# <code>squeue -u <username> </code> List all running jobs for a user
# 
# <code>scancel <jobid></code> Cancel a single job 
# 
# For more information about slurm files and scheduling these jobs, check out these following websites <a href=" https://slurm.schedmd.com/pdfs/summary.pdf"> Cheat sheet Slurm Workload Manager </a> , <a href=" https://docs.rc.fas.harvard.edu/kb/convenient-slurm-commands/">Convenient SLURM Commands</a>, and  <a href=" https://slurm.schedmd.com/sbatch.html "> Slurm Documentation </a>
# 
# 

# ## **Querying the Data with Datasette.io** 
# 
# ### **Accessing the Data with Datasette**
# 
# In order to make our database more intuitive and accessible, we use the “datasette” module to create a high-level dashboard. This dashboard contains the data in a table format. It also presents drop down lists in order to select and subset data of interest. The datasette module also allows you to download the data in a CSV file or a JSON file. In this section, we discuss setting up this datasette module on Rivanna and how to access this module each time you want to download data of interest. 
# 
# Before accessing the drop-down menu and high-level dashboard, you would need to import the datasette module. This module is open source, and can be imported on Rivanna. In the overview below, steps 1-2 walk through installing this module. Steps 3-8 are for accessing and parsing through the data. 
# 
# ***High level datasette.io procedure***
# 1.	Log onto Rivanna
# 2.	If first time importing module start here, if not skip to step 3:
# a.	Start a session on Jupyter session on project space
# b.	Open a terminal 
# c.	Make sure you are in your home directory (cd)
# d.	Type in “pip install --user datasette”
# i.	Should be installed in home directory
# 3.	Start a Desktop session on Rivanna
# 4.	Open a terminal window 
# 5.	Type in this: ~/.local/bin/datasette “/path-to-database/database-name.db”
# a.	Make sure you include the first slash and double quotes!
# 6.	It should start a port local connection. Copy connection link and open in firefox
# 7.	Click on table name in datasette.io interface
# 8.	You can now make queries through a dropdown menu and download the csv file
# 
# 
# Rivanna is the University of Virginia’s high performance computing platform. This means that instead of using your local computer and storage, you can work and share files on this platform. When we are working with a lot of data — like in the case of this automated data pipeline — Rivanna provides more storage and a centralized place to collaborate. To log onto Rivanna, go to UVA’s research computing website and select <a href=" https://www.rc.virginia.edu/userinfo/rivanna/login/ ">Rivanna</a>
# 
# 
# There, click on the link that says “Launch Open OnDemand”. Log into this system with your UVA ID and associated password. Once on Rivanna, click on “My Interactive Session” on the top menu bar. Then, we can select which Interactive App you would like to use. For this project, we mainly use JupyterLab — a coding interface typically used for Python. We will also use the Desktop application to access the high-level dashboard we create. When using Rivanna, you have the option of customizing the number of hours you plan on working on the system, as well as the number of cores you would need. 
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/Datasette_1.jpg" width=550 height=500 />
# 
# 
# To set up the datasette module, log onto Rivanna. This only needs to be done once per user (computing ID). The steps to log onto Rivanna are in chapter XX. Select the JupyterLab interactive app. Some options will appear. Leave the options as below, changing the allocation name to the project space of interest. 
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/Datasette_2.jpg" width=500 height= 500 />
# 
# Launch the app, and create a new terminal session. 
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/Datasette_3.jpg" width=550 height=500 />
# 
# Next, type “cd” into the terminal. This makes sure you are working in your home directory. Next, type “pip install --user datasette”. This will install the datasette module. 
# 
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/Datasette_4.jpg" width=550 height=500 />
# 
# 
# The next steps are steps to access the datasette module. This is steps 3 onwards in the overview above. To access the datasette module, go back to “My Interactive Sessions” on Rivanna. Open a “Desktop” session, leaving changing the allocations to the number of hours of interest. With the Desktop application, you can slide the “Image Quality” bar to “high” to make the desktop less pixelated. 
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/Datasette_5.jpg" width=550 height= 500 />
# 
# 
# Launch the Desktop application. To copy and paste into this environment, you have to use the side-menu clipboard. This is highlighted in the image below.
# 
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/Datasette_6.jpg" width=550 height= 500 />
# 
# 
# Open a terminal window in the Desktop application. Copy and paste this command into the desktop: ~/.local/bin/datasette “/project/path-to-database/database-name.db”. Make sure you are using double quotes for the path to where the database exists. Also, make sure to include the initial forward slash, and the project to indicate the database exists in a project space on Rivanna. Paste on the desktop terminal, and hit enter. 
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/Datasette_7.jpg" width=500 height=500 />
# 
# A link to a server containing the dashboard should appear. Copy and paste this link into firefox on the Desktop application. 
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/Datasette_8.jpg" width=550 height=500 />
# 
# Click on the “item_specs” table. This is the table containing the data that is collected everyday at midnight. We can use the drop down menu that appears to filter the table to your liking. You can also leave the drop down menu blank to collect all the data. In this example, we filter for items of Price greater than $1000. 
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/Datasette_9.jpg" width=550 height=500 />
# 
# 
# To download the data as a CSV file, right click on the “CSV” link, and click “Save Link As”. This will result in a window where you can choose where to download the dataset of interest. Select where you would like to save the CSV file, rename the file to your liking, and click save. In this example, we save it to the Rivanna Desktop. 
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/Datasette_10.jpg" width=550 height=500 />
# 
# To shut down Desktop, simply close out of Firefox. In the terminal window that is open, hit control-C on your keyboard. This should result in the server shutting down. 
# 
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/Datasette_11.jpg" width=550 height=500 />
# 
# 
# The data now lives in your home directory on Rivanna in CSV format. To access this data, go back to the Jupyter application, select “HOME” as your work directory, and start a session. 
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/Datasette_12.jpg" width=500 height=500 />
# 
# Once the session begins, you should be able to find the data in the file you chose earlier in the Desktop application. In this example, it exists in the “Desktop folder”. You can right click on the CSV file to download it onto your local computer. 
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/Datasette_13.jpg" width=550 height=500 />
# 
# You now have the most up to date version of the dataset of your liking! You can use this CSV file for analysis in R, Python, STATA or other software of your choice. The data will keep being collected, and new data can be accessed with the same steps. 

# ### **Final Remarks**
# 
# This documentation provides a detailed and comprehensive overview of the implementation of a data pipeline for social research. This data pipeline makes a connection to eBay’s developer’s program, connects to the appropriate APIs, collects data, and stores data. This pipeline also provides a dashboard for accessing and saving the data for future works. When editing the data pipeline, the “Navigating the Code” chapter will be useful in understanding the specific implementation of Python code. General Python errors that appear can be researched on Google or StakeOverflow. Connection errors to eBay’s developer program can be researched on eBay’s documentation. The implementation of this data pipeline will allow for social search to collect up-to-date data on categories of interest across eBay, and can be edited for more specific use-cases. 

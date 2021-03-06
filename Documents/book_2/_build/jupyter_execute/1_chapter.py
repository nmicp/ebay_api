#!/usr/bin/env python
# coding: utf-8

# ## **Preliminaries**
# 
# ### **Description of eBay's API Data Pipeline** 
# 
# #### **General Workflow of eBay’s Data Pipeline**
# 
# 
# The following flowcharts should help navigate the process of building the data pipeline. Specifics will not be highlighted in the roadmap, but will reference future chapters that dive into each section. Definitions of technical terms in this diagram can be found in chapter 1.
# 
# *Figure 1*  highlights the general structure of how we built out this eBay data pipeline for research. The first step of getting data from eBay’s developer’s program was to get API keys. The steps of collecting these keys are described in the Understanding API chapter while the implementation of a Flask app is in chapter 3. This connection will only need to be completed once per project.
# 
# Next, we build the data pipeline in python script. This is highlighted in steps B through D - see the below diagrams. This recursive data collection method runs every 24 hours to collect the most up-to-date data from eBay categories of interest. This general procedure ranges from collecting the access keys to running an automated script. This algorithm consists of three main activities in an automated fashion: connecting to the desired API (Shopping and Finding API), mining the data, and saving the information in a SQL database. Specific background knowledge on these steps can be found in chapter “Getting Started with eBay’s API”. Implementation of this framework in python can be found in “Getting Data from eBay”. The last step of the roadmap — analysis — is open for social research. In the previous steps, we set-up a pipeline that cleans and stores data that is accessible through a csv file. In the analysis section, this csv file can be downloaded to be used in future analysis and research. Information on how to access the data for analysis can be found in “Accessing Data with Datasette”. 
# 
# *Figure 1.*     Flowchart of eBay's Data Pipeline
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/fig1.jpg" width=200 height=500 />
# 
# This section provides a high-level overview of each of the critical stages in the data collection and processing pipeline. More information about each step will be discussed in the following chapters. 
# 
# **Diagram A** outlines the necessary steps to make an initial connection to eBay's API system and gain access to their data. First, interested parties are required to create a developer's program and apply for application access keys. They are then required to construct a RESTful API to communicate with eBay's system and receive developer tokens. These tokens are unique and should be stored in a secret .env file located in the same directory as the other project scripts. More information regarding getting access to eBay’s API can be found in the beginning of chapter 3. 
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/fig2.jpg" width=400 height=280 />
# 
# **Diagram B** describes the need of having a basic understanding of the functions of eBay’s API and documentation. In general, once a successful connection to eBay has been established, users will need to read through and understand eBay's documentation and syntax to interface with APIs of interest. For our use case, the Finding and Shopping APIs to get data for our features of interest. More specific information about the language of the eBay developer’s program can be found in chapter 2. 
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/fig3.jpg" width=300 height=380 />
# 
# **Diagram C** provides an overview on the method of how data is extracted and cleaned. The extracted raw data is converted to a tabular format, and other cleaning processes are performed using a series of nested loops. Details on the code that implements this can be found in chapter 3. This section describes the recursive nature that is completed automatically every day when script runs to collect data from eBay. 
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/fig4.jpg" width=300 height=380 />
# 
# **Diagram D** provides a framework for data storage and retrieval. Once the data has been successfully processed into a clean table, we store it for later use. A permanent storage space comes in the form of tables in a dedicated SQL database. If the table does not exist, it must be created. However, if the table already exists then the processed data is simply appended to it. We create a table once, and keep updating the table with the newest data we collect each day. This recursive nature of storing data can be found in chapter 3. 
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/fig5.jpg" width=300 height=380 />
# 

# ### **Key Concepts** 
# 
# This chapter aims to explain key concepts essential to the automated data collection process through eBay’s API. 
# 
# **1) Data Types:**
# 
# Data types are an important aspect in programming that help determine the type of the object’s value. Some examples include numeric, alphanumeric, decimal values. Their differences lie in the types of operations the computer system can perform.    
# 
# There are a variety of data types. Generally, data types can be classified into two categories: primitive/structure and composite. Primitive data types are native to the processor; they have a one-to-one correspondence with objects in the computer’s memory (a common data type of this class is an integer – whole number). Composite data types are constructed in the program out of primitive data types and other aggregate data types. A dictionary is an example of this category. 
# 
# To avoid confusion, let us start by describing the main data types used in the eBay documentation and how these concepts might differ from ordinary use. For example, the use of float and decimal types in the world of programming and in eBay's APIs may differ. Intuitively, we may think that a float is used as a decimal number in the calculator; however, an eBay decimal type contains different elements that are not necessarily numbers separated by decimal points. Therefore, as the meanings of data types can vary, we will explain them throughout this manual.
# 
# <div class="alert alert-block alert-info"><b>Tip:</b> Missing data on eBay results in the key:value pairs sometimes not existing for specific listings. Missing data from eBay results in missing data in the dataframe. This missing data is read into the python table as a missing data type. However, when stored into a SQL database, this variable type is changed into a string (words) that state “None”. Since SQL databases do not allow missing rows, we substitute this as a word highlighting missing data. In future analysis, one can filter the “None” text to remove missing values.</div>
# 
# In the following table presents eBay’s schema types with examples:
# 
# *Table 1.* Primitive Data Types with examples 
# 
# 
# |     Data   Type    |     Description                                                                                                                                                                                                                                                                                                                                                   |     Example                                                                                                                                      |
# |--------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------|
# |     String         |     contains one or   more characters, which can include numbers, letters, and other terms. The use   of quotes ‘’ or double “” ensures that the element can be recognized as a   string.                                                                                                                                                                         |     <code>Item_ID</code>           <code><CategoryParent>string </CategoryParent></code>                                                         |
# |     Boolean        |     represents   binary-valued logic with values of true   or false. These can be   represented as 0 (for false) and 1(for true).                                                                                                                                                                                                                                 |     <code> {true, false}</code>           <code> {1, 0}</code>                                                                                   |
# |     Int            |     An integer is a   numeric value without a decimal point. Integers are whole numbers; they can   be positive, negative, or zero.                                                                                                                                                                                                                               |     <code>-1, 0,   126789675, +100000</code>                                                                                                     |
# |     Float          |     A number with a   decimal point using 32 bit data (whole numbers may omit the decimal point).   By using a float you can control where to locate the decimal point.                                                                                                                                                                                           |     <code> 1E4, 1267.43233E12, 12.78e-2, 12 , -0, 0 </code>     <code>INF </code>                                                                |
# |     Double         |     A number with a   decimal point using 64 bit data. Double float number may  contain the digits 0-9, a hyphen to   designate negative numbers, and a period (“.”) as the decimal separator. A   common application is monetary values                                                                                                                          |     <code>12678967.543233</code>                                                                                                                 |
# |     Decimal        |     In contrast to   float and double, which use rounding, decimal preserves all the digits.                                                                                                                                                                                                                                                                      |     <code>   -1.23,+100000.00, 210.      </code>                                                                                                 |
# |     dateTime       |     It stores a   specific instant of time (start and end times). Its format is YYYY-MM-DD and   it records Universal Coordinated Time (UTC). Alternatively, it can represent   the official eBay time.                                                                                                                                                           |     <code> 2022-01-10T12:00:00-05:00</code>           2022-01-10T17:00:00Z,   five hours later than 2022-01-10T12:00:00Z.                        |
# |     Duration       |     It contains a   length of time and usually conveys the time left before a listing ends. Their   format is as follows:     P (period),     nY (number of   years).     nM (number of   months)     nD (number of   days),      T (date/time   separator),     nH (number of   hours),      nM (number of   minutes),     nS (the number   of seconds)          |     <code>PnYnMnDTnH nMnS   </code>            (e.g., P2DT23H32M51S)      “ period of 2 days, 23   hours, 32 minutes, and 51 seconds”.           |
# 
# 
# For explanatory purposes, the documentation of the different eBay APIs includes several composite data types. Here we will focus on the types most used in the shopping API.
# 
# *Table 2.* Composite Data Types with examples:
# 
# |     Data Type             |     Description                                                                                                                                                                                                                                                                                                                                                                   |     Example                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
# |---------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
# |     Dictionary            |     It is a collection of key values (unique identifier) that refer   to objects. Each key is associated with only one item, so it can be used to   find a particular set of data. Typically, keys are simple datatypes – usually   alphanumeric strings.            A dictionary data type can support operations, such as   retrieving, inserting, or updating values.          |     # empty dictionary     <code>my_dict   = {}</code>           # dictionary with integer keys     <code>my_dict = {1: 'orange', 2:   'ball'}</code>           # dictionary with mixed keys     <code> my_dict = {'name': 'Nick', 1: [2, 4,   3]}</code>           # using dict()     <code>my_dict =dict({1:'lemon',   2:'rule'})</code>           # from sequence having each item as a pair     <code>my_dict =   dict([(1,'orange'),(2,'ball')])</code>    |
# |     token                 |     A token is an abbreviation   in which white spaces are removed.                                                                                                                                                                                                                                                                                                               |     <code><ShippingServiceName> token</ShippingServiceName></code>                                                                                                                                                                                                                                                                                                                                                                                              |
# |     AmountType            |     It is a double   type (64 bit) that specifies a monetary value – fees, prices, etc. - and   currency.                                                                                                                                                                                                                                                                         |     <code><Group1MaxFlatShippingCostcurrencyID="CurrencyCodeType"> AmountType (double)</Group1MaxFlatShippingCost></code>                                                                                                                                                                                                                                                                                                                                       |
# |     CountryCodeType       |     It is a token   data type that contains two-letter country codes.                                                                                                                                                                                                                                                                                                             |     <code><DestinationPostalCode> string</DestinationPostalCode></code>                                                                                                                                                                                                                                                                                                                                                                                         |
# 
# **2) Application Programming Interface (API):**
# 
# API is the acronym for Application Programming Interface. APIs serve as intermediaries through an online connection or set of programming codes. For example: a server receives a data query, parses responses, and sends instructions between a data provider and an end-user.  
# 
# To perform this intermediary role, APIs use standards, such as Hypertext Transfer Protocol (HTTP), and other Internet applications. APIs use different types of files to access information, such as XML and JSON format files. We will explain those file types in future sections.  
#  
# 
# 
# **3) Extensible Msrkup Languaje (XML):**
# 
# XML stands for eXtensible Markup Language. We use it to store and transport data. XML facilitates communication between humans and machines. Due to its easy-to-read to read format, it is widely developed in APIs. This language uses a serialization process (translating a data type into a format that can be easily stored or transmitted over a computer network to be later reconstructed in a different environment). The versatility of this format is highly appealing in the API data collection.    
# 
# **4) JSON Format:**
# 
# JSON is a text-based data format for storing and exchanging information.  JSON data are used to send HTTP requests between applications. They are structured as a collection of key-value pairs, in which the key must be a type string followed by one of the following data types: numbers, boolean, array, etc. (See description of data types)
# 
# There are two valid types of JSON formats: a collection of key-value pairs enclosed by curly braces {}, or an ordered list of key-value pairs separated by commas and enclosed by a pair of square brackets []. See examples at this link: 
# 
# 
# <a href="https://developer.ebay.com/devzone/finding/CallRef/Samples/findItemsByCategory_basic_out_json.txt">JSON Format Samples</a>
# 
# 
# **5) Simple Linux Utility for Resource Management (Slurm):**
# 
# Slurm Workload Manager is a free and open-resource job scheduler for Linux and Unix-Like kernels. <a href="https://www.rc.virginia.edu/userinfo/rivanna/slurm/" target="_blank">(Slurm)</a> allows users to prepare their computational workloads, or jobs, on allocated nodes to send them to a job controller. The controller oversees running on login nodes, scheduling, and monitoring the jobs in each period.
# 
# Slurm makes it easy for users to perform jobs in an automated manner in a time frame without the need to be present to review the process. For example, we scheduled a job to acquire seniority data for this capstone project starting at midnight. This facilitated the data collection, given the company’s policy of restricting daily calls to the Shopping API to 5,000 calls.
# 
# 
# **6) SQL database:**
# 
# Structured Query Language -SQL- is used to manage relational databases. A <a href="https://jkropko.github.io/surfing-the-data-pipeline/ch7.html" target="_blank"> relational data model</a> involves the use of data tables that collect groups of elements into relations. Each table contains columns and rows with a primary key identifying each row. Columns are attributes of labeled elements. Rows represent single items that belong to a type of entity.  The organization of a relational database must provide derivability, redundancy, and consistency in the data. See *figure 2* below
# 
# 
# *Figure 2*. Feature schema for Item table stored in SQLite database 
# 
# <img src="https://raw.githubusercontent.com/nmicp/ebay_api/master/Documents/book_2/fig6.jpg" width=300 height=280 />
# 
# **7) Flask Application:**
# 
# Flask is a lightweight Python web framework that provides useful tools and features for creating web applications in the Python language. We implement a flask application to connect to eBay’s API. The specific implementation can be found in the next chapter. 

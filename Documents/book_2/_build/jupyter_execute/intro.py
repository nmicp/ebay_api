#!/usr/bin/env python
# coding: utf-8

# # Welcome to eBay’s API Data Pipeline
# 
# ### **What Is this Manual About?** 
# 
# This manual aims to provide technical guidance and documentation to the process of building an automated data pipeline from eBay’s developer’s program for research purposes. Specific technical documentation will walk through the process of accessing eBay's Application Programming Interface (API), and documenting the code that collects the data. This is a product of the capstone project, "Network Mobility of Illicit Cultural Property" developed by the UVA Data Science School and the <a href="https://curialab.org/">Cultural Resilience Informatics and Analysis (CURIA) Lab</a>.
#  
# This research project stems from research of online marketplace as platforms for illicit trade. The scale of global art crime has been difficult to quantify due to the vast number of transactions and varying methods of trade. The illicit antiquities trade has moved away from physical specialist shops in favor of online buying and selling platforms such as eBay. These online platforms characterized by transactions and vendors offering heterogeneous goods have not been systematically studied due to its data-intensive nature. This project designs a robust data pipeline that collects, processes, and stores data to quantify and analyze the network mobility of illicit cultural property. The data pipeline consists of a template for accessing eBay’s API, understanding API documentation, and collecting necessary features for future analysis. The metadata for building and maintaining the data pipeline is recorded in an in-depth guide to account for data collection bias. 
# 
# In this documentation we organize the use-case of this data pipeline in the following manner.
# 
# **Chapter 1: Preliminaries** 
# 
# This documentation begins by explaining the basic technological concepts needed to build an API. This chapter will also include a dictionary of the eBay categories used to extract the necessary data from the listings in the antiques categories. The chapter includes a data modeling section that explains the SQL schema of building a relational database. 
# 
# **Chapter 2: Getting Started with eBay’s APIs**
# 
# The second chapter provides a theoretical framework of picking these APIs, data description, and a section of legal and ethical challenges will also be included in this chapter. This is a user-friendly and comprehensive description of eBay's API documentation, focused on the Shopping and the Finding APIs.
# 
# **Chapter 3: Getting Data from eBay**
# 
# Finally, the third chapter focuses on the specific implementation of the data pipeline architecture in python. This chapter includes a step-by-step guide on how to obtain this data from a recursive script, and also a tutorial to run these activities from the Rivanna UVA platform that facilitates the data storage systems. The result of this data pipeline framework is a replicable blueprint for interacting with an online marketplace’s API environment. This project will act as a precursor to begin research regarding the global trade of illicit cultural property through subsequent network and spatial analysis. 
# 
# The updated version of this manual is 2022-05-10. 
# 

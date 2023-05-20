Overview:
This project is divided into two parts; the climate analysis of Honolulu in Hawaii based on seven different active station and precipitation of those station and  Flask API based on the queries in climate analysis. 

Scope: 
This report focuses on the climate database extracted from Honolulu which includes data from 7 different active station in Honolulu along with its temperature and precipitation among the different dates.

Methodology:
Performing the basic climate analysis and data exploration of Honolulu climate database with the use Python and SQL Alchemy including SQL Alchemy queries, Pandas and Matplotlib.    

Precipitation Findings:
1.	Recent date in dataset.
2.	Precipitation data of previous 12 months.
3.	DataFrame values sort by date. 
4.	Graph for precipitation (y-axis) and date (x-axis) from 23/08/2016 To 10/07/2017.   
5.	Summary statistics of precipitation data.

Station Findings:
1.	Total number of stations in the dataset. 
2.	The most active station in dataset based on the times it appear in the dataset – including its lowest, highest and average temperature.
3.	The station that has the greated number of observation. 
4.	Graph for temperature and frequency. 

Conclusion: 
With the use of Python SQL toolkit and Object Relational Mapper I were able to create a engine to reflect the existing database into a new model. Based on that I were able to automap 2 classes in the Hawaii sqlite dataset and they are Measurement and station. Moreover, Exploratory Precipitation and Station Analysis is performed which you are able to view in the findings part. In addition, Flask API app is created to answer the queries from the analysis part. 

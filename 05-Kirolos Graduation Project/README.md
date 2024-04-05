# BIG DATA PROJECT: COVID-19 ANALYSIS
**DATA ENGINEERING MASTERCLASS** 

**Project Done by: Kirolos Samir Yossif Girgis**

This is the capstone project for Sprints' data engineering masterclass presented to Engs. Amr Saleh Ahmed Reda. The project focuses on analyzing COVID-19 data using big data technologies. The Project was Originally planned to be implemented with Cloudera QuickStart VM, HDFS, Hive, and Oozie to provide a comprehensive solution for processing and analyzing large datasets using the Cloudera ecosystem, and then visualize the output data using Microsoft Power BI. However, this plan encountered many configuration issues that prevented its continuity. As a result, the project was redesigned to employ AWS services including S3, Glue, and Redshift to accomplish the data analysis tasks.

# Original Plan
## Prerequisites and Features

Before getting started with this project, ensure that you have the following components set up:

1. **Cloudera QuickStart VM**: Download and install the Cloudera QuickStart VM, which provides a pre-configured environment for running Hadoop, Hive, and Oozie.

The project includes the following features:

1. **HDFS (Hadoop Distributed File System)**: Utilize HDFS for storing and managing covid-19 dataset into HDFS directory /ds containing /COVID_HDFS_LZ as a sub-directory.

2. **Hive**: Leverage Hive, a data warehouse infrastructure, to provide a high-level query language for data analysis and manipulation.

3. **Hue**: Use Hue, a web-based interface, to interact with the Cloudera ecosystem components, including Hive, and HDFS, through a user-friendly graphical interface.

4. **Oozie**: Employ Oozie, a workflow scheduler system, to manage and orchestrate complex data processing workflows in Hadoop.

## Getting Started

1. Start the Cloudera QuickStart VM and ensure that all the necessary services, such as HDFS, Hive, Hue, and Oozie, are running.

2. Create a Folder on the VM named "/home/cloudera/covid_project".

3. Create folders under "covid_project" named "landing_zone" and "scripts".

4. Import "covid-19.csv" file into the Cloudera VM using WinSCP into "landing_zone" folder.

5. Import the dataset into HDFS directory named "COVID_SRC_LZ" using Load_COVID_TO_HDFS.sh file.

        #!/bin/bash

        #Landing Zones in Linux and HDFS
        LINUX_LANDING_AREA=/home/cloudera/covid_project/landing_zone
        HDFS_LZ=/user/cloudera/ds/COVID_HDFS_LZ

        echo "GLOBAL Variables= " $LINUX_LANDING_AREA ", " $HDFS_LZ 

        hdfs dfs -mkdir -p $HDFS_LZ
        echo "COVID_HDFS_LZ CREATED successfully"


        hdfs dfs -put $LINUX_LANDING_AREA/covid-19.csv $HDFS_LZ
        echo "covid-19.csv dataset LOADED successfully"

6. Utilize Hue to interact with the Hive editor through a web-based interface to create a database named "covid_db" and schema for a staging table named "covid_staging" with the following code:

        CREATE TABLE IF NOT EXISTS covid_db.covid_staging 
        (
        Country 			                STRING,
        Total_Cases   		                DOUBLE,
        New_Cases    		                DOUBLE,
        Total_Deaths                       DOUBLE,
        New_Deaths                         DOUBLE,
        Total_Recovered                    DOUBLE,
        Active_Cases                       DOUBLE,
        Serious		                  	DOUBLE,
        Tot_Cases                   		DOUBLE,
        Deaths                      		DOUBLE,
        Total_Tests                   		DOUBLE,
        Tests			                 	DOUBLE,
        CASES_per_Test                     DOUBLE,
        Death_in_Closed_Cases     	        DOUBLE,
        Rank_by_Testing_Rate 		        DOUBLE,
        Rank_by_Death_Rate    		        DOUBLE,
        Rank_by_Cases_Rate    		        DOUBLE,
        Rank_by_Death_of_Closed_Cases   	DOUBLE
        )
        ROW FORMAT DELIMITED FIELDS TERMINATED by ','
        STORED as TEXTFILE
        LOCATION '/user/cloudera/ds/COVID_HDFS_LZ'
        tblproperties ("skip.header.line.count"="1");

7. Create Hive ORC table named "covid_partitioned" that is partitioned by country and data are loaded dynamically into it to speed up query using the following code:

        SET hive.exec.dynamic.partition = true;
        SET hive.exec.dynamic.partition.mode = nonstrict;
        SET hive.exec.max.dynamic.partitions=100000;
        SET hive.exec.max.dynamic.partitions.pernode=100000;

        CREATE EXTERNAL TABLE IF NOT EXISTS covid_db.covid_ds_partitioned 
        (
        Country 			                STRING,
        Total_Cases   		                DOUBLE,
        New_Cases    		                DOUBLE,
        Total_Deaths                       DOUBLE,
        New_Deaths                         DOUBLE,
        Total_Recovered                    DOUBLE,
        Active_Cases                       DOUBLE,
        Serious		                  	DOUBLE,
        Tot_Cases                   		DOUBLE,
        Deaths                      		DOUBLE,
        Total_Tests                   		DOUBLE,
        Tests			                 	DOUBLE,
        CASES_per_Test                     DOUBLE,
        Death_in_Closed_Cases     	        DOUBLE,
        Rank_by_Testing_Rate 		        DOUBLE,
        Rank_by_Death_Rate    		        DOUBLE,
        Rank_by_Cases_Rate    		        DOUBLE,
        Rank_by_Death_of_Closed_Cases   	DOUBLE
        )
        PARTITIONED BY (COUNTRY_NAME STRING)
        STORED as ORC
        LOCATION '/user/cloudera/ds/COVID_HDFS_PARTITIONED'
        tblproperties ("skip.header.line.count"="1");

        INSERT INTO TABLE covid_db.covid_ds_partitioned PARTITION(COUNTRY_NAME)
        SELECT *,Country FROM covid_db.covid_staging WHERE Country is not null;

8. Create Hive table named "covid_final_output" to generate the final report which will generate an output file to be visualized.

9. Create an Oozie workflow action using Hue to run the HDFS shell script and execute the hive queries. 

10. Run the Oozie workflow job manually from the Hue to get the final output.

11. Pick the generated final output file from HDFS file location and download it to be visualized using Power BI.


## Configuration Issues Faced

1. **Permission denied when running Load_COVID_TO_HDFS.sh file.**

    To overcome this issue, the following need to be executed to provide execute and read permission to the .sh file.

        chmod u+rx Load_COVID_TO_HDFS.sh

2. **Hive keeps crashing when running**

    After reviewing the log for these failed attempts. The following error appeared:
    
        org.apache.hadoop.mapred.YarnChild: Error running child : java.lang.OutOfMemoryError: Java heap space
    
    To overcome this issue, I tried many solutions till it worked, such as:
    - Using different versions of Cloudera Quickstart VM (5.4.2, 5.12.0, 5.13.0)
    - Using more RAM (from 8 to 12 GB)
    - Changing some configuration in Cloudera Management, such as changing mapred.java.child.opts, mapred.child.ulimit, and mapred.tasktracker.map.tasks.maximum.

3. **Creating external table keeps running with map = 0% and reduce = 0% indefinitely**

    After trying many solutions for this error, I was stuck and had to change the whole plan to finish this project. **AWS Services were the selected alternative for the whole project as it provides the required platforms in addition to being a required skill in the data engineering field.**

# Alternative Plan Using AWS Services
## Prerequisites and Features

Before beginning the project, ensure the following prerequisites are met:

1. **AWS Account**: Set up an AWS account to access the required services.

2. **Microsoft Power BI Desktop**: Download and install the Microsoft Power BI Desktop application.

The project includes the following features:

1. **AWS S3 (Simple Storage Service)**: Utilize S3 to store and manage COVID-19 datasets in a scalable and durable object storage service.

2. **AWS IAM(Identity and Access Management)**: Utilize IAM role for managing user access to AWS resources. IAM allows you to control and secure access to your AWS services, including S3, Glue, and Redshift.

3. **AWS Glue**: Leverage Glue to perform ETL (Extract, Transform, Load) operations on the COVID-19 data, enabling data preparation and transformation for analysis. Glue simplifies the process of discovering, transforming, and moving data between different data sources.

4. **Amazon Redshift**: Utilize Redshift, a fully managed data warehousing service, to store and analyze large volumes of COVID-19 data efficiently.

5. **Microsoft Power BI**: A powerful business intelligence and data visualization platform that will visualise and report the COVID-19 data.


## Getting Started

### 1. Data Storage

- Create  S3 bucket in AWS account named "covid-project-1" that contains two subfolders named "/csv" and "/output".
- Upload "covid-19.csv" files to the S3 bucket "/covid-project-1/csv/".

### 2. Data Ingestion, Process and Transformation

- Create an AWS Glue data catalogue to define the schema and metadata for your COVID-19 data.
- Create Glue crawlers named "S3-to-Glue" to automatically discover and catalogue "covid-19.csv" data stored in the S3 bucket.
- Create IAM role named "AWSGlueServiceRole" and policies to define fine-grained access controls for different users or groups.
- Assign appropriate IAM permissions to access the AWS services used in the project (S3, Glue, Redshift) based on the user's role and responsibilities.
- Create an AWS Redshift serverless workgroup named "covid-project" cluster to serve as the data warehousing solution.
- Configure a Virtual Private Cloud (VPC), VPC security group, and subnets.
- Create a namespace named “covid-19” that contains public database and dev schema.
- Associating IAM role in the permissions that allow Redshift to have full access to S3 and Glue.
- Define the appropriate schema in Redshift to match the transformed data from Glue by Navigating to Redshift Query editor and create a new table in the public database and dev schema named “covid_staging” with the following code:

        CREATE TABLE IF NOT EXISTS covid_staging 
        (
        Country 			                VARCHAR,
        Total_Cases   		                DOUBLE PRECISION,
        New_Cases    		                DOUBLE PRECISION,
        Total_Deaths                       DOUBLE PRECISION,
        New_Deaths                         DOUBLE PRECISION,
        Total_Recovered                    DOUBLE PRECISION,
        Active_Cases                       DOUBLE PRECISION,
        Serious		                  	DOUBLE PRECISION,
        Tot_Cases                   		DOUBLE PRECISION,
        Deaths                      		DOUBLE PRECISION,
        Total_Tests                   		DOUBLE PRECISION,
        Tests			                 	DOUBLE PRECISION,
        CASES_per_Test                     DOUBLE PRECISION,
        Death_in_Closed_Cases     	        DOUBLE PRECISION,
        Rank_by_Testing_rate 		        DOUBLE PRECISION,
        Rank_by_Death_rate    		        DOUBLE PRECISION,
        Rank_by_Cases_rate    		        DOUBLE PRECISION,
        Rank_by_Death_of_Closed_Cases   	DOUBLE PRECISION
        );

 
- Creating an AWS Glue job to perform ETL operations on the COVID-19 data from S3 into Redshift. Define data transformations and mappings as necessary.
- Execute the Glue job to extract, transform, and load the COVID-19 data into Redshift.

### 3. Data Analysis

- Create another AWS Glue job that uses Redshift table and sort and order it by deaths and tests and then load it to new external tables in Redshift.

- Execute the Glue job to extract, transform, and load the COVID-19 data into Redshift.

- Utilize Redshift to execute queries and perform data analysis on the COVID-19 datasets.

- Utilize Redshift to unload the output data from Redshift to S3 Bucket "/covid-project-1/output" using the following code:

        UNLOAD ('SELECT * FROM deaths ORDER BY deaths DESC')
        TO 's3://covid-project-1/output/'
        IAM_ROLE 'arn:aws:iam::992382770258:role/AWSGlueServiceRole' csv
        PARALLEL OFF;


        UNLOAD ('SELECT * FROM deaths ORDER BY deaths DESC')
        TO 's3://covid-project-1/output/'
        IAM_ROLE 'arn:aws:iam::992382770258:role/AWSGlueServiceRole' csv
        PARALLEL OFF;

### 4. Data Visualization

- Visualize the results using visualization tools Microsoft Power BI and create a dashboard to be presented.

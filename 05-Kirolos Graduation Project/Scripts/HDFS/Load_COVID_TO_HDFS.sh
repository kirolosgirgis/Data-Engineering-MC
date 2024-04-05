#!/bin/bash

#Landing Zones in Linux and HDFS
LINUX_LANDING_AREA=/home/cloudera/covid_project/landing_zone
HDFS_LZ=/user/cloudera/ds/COVID_HDFS_LZ

echo "GLOBAL Variables= " $LINUX_LANDING_AREA ", " $HDFS_LZ 

hdfs dfs -mkdir -p $HDFS_LZ
echo "COVID_HDFS_LZ CREATED sucessfully"


hdfs dfs -put $LINUX_LANDING_AREA/covid-19.csv $HDFS_LZ
echo "covid-19.csv dataset LOADED sucessfully"

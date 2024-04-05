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


UNLOAD ('SELECT * FROM deaths ORDER BY deaths DESC')
TO 's3://covid-project-1/output/'
IAM_ROLE 'arn:aws:iam::992382770258:role/AWSGlueServiceRole' csv
PARALLEL OFF;


UNLOAD ('SELECT * FROM deaths ORDER BY deaths DESC')
TO 's3://covid-project-1/output/'
IAM_ROLE 'arn:aws:iam::992382770258:role/AWSGlueServiceRole' csv
PARALLEL OFF;
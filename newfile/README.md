# Log Analysis
This is project one for Udacity Full Stack ND.

## Overview
This project's main objective to get you to understand and run postgresql commands. There are three questions the student has to answer.  
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time? 
3. On which days did more than 1% of requests lead to errors?

## Requirements
* python 2.7
* psycopg2
* news sql file - provided by Udacity. 
* Vagrant

```
pip install psycopg2
```

## How to Run
You will need to first install vagrant.  
You can download from this [link](https://www.vagrantup.com/downloads.html). Once this is done, Udactiy provides the data for the news data. This will need to unzipped in the vagrant dir. 

Once you have vagrant downloaded and data unzipped, you can activate vagrant with the following steps. 

```
vagrant up - to start you vm.
vagrant ssh - to connect to the vm.
vagrant halt - to "turn off" the vm.
```
Clone or unzip the GIT repo in your vagrant dir.  
Your working dir will be under '/vagrant' after you ssh in. Navigate to your news data and run the following command. 

```
psql -d news -f newsdata.sql
```
psql - The Postgresql command line.  
-d news - connect to the database named news (This is provided from Udacity).  
-f newsdata.sql - run the sql statements in the file newsdata.sql  

psql - The Postgresql command line.  
-d news - connect to the database named news (This is provided from Udacity).  
-f newsdata.sql - run the sql statements in the file newsdata.sql  

Once you have configured your workspace, you can then move on to developing your query and python program.  
You can test out the queries by running the following command: 
```
psql news
you will be able to run SELECT commands. 
\d - view all tables. 
\d+ <table name> - views columns in the table. 
\q to exit out of psql cli.
```

## Code Design
The code will first dispaly options for the user to choose. 
Main method is responsible for calling other methods and passing values in. 

## Run Code
Type the following command: 
```
python news.py 
```
You will be prompted with four options. Options 1-3 will allow you to execute individual query. Option 4- will execute all three quries. 
Keep in mind that theses results take a little time to display.


## Author
Jay Shah

### Resource 
I would like to thank memebers of the fsnd slack community for helping with SQL.

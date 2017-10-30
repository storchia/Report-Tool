# Reporting Tool
Reporting Tool is a basic tool that will run reports from the news database.

##### Author
Sergio A. Torchia
**Contact:** sergiotorchia@hotmail.com

## Database Description
Is a PostgreSQL database for a fictional news website.
The database includes three tables:

- The authors table includes information about the authors of articles.
- The articles table includes the articles themselves.
- The log table includes one entry for each time a user has accessed the site.

## Reporting Tool Description
Report Tool will provide you three reports individually or all together based on your selection.
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## How to access DB and run the Reporting Tool
Reporting tool works on a Linux-based virtual machine (VM) if you don't have it you can download it  [here](https://www.vagrantup.com/intro/getting-started/install.html).
In case you need to install VM Virtual Box, you can find it
[here](https://www.virtualbox.org/wiki/Downloads).
In order to **power up and connect** to the VM:
1. From the command line, navigate to the folder containing the Vagrantfile
2. Power up the virtual machine by typing: vagrant up note: this may take a couple minutes to complete
3. Once the virtual machine is done booting, log into it by typing: vagrant ssh
4. [Download this file](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). You will need to unzip this file after downloading it. The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine. To load the data, `cd `into the vagrant directory and use the command `psql -d news -f newsdata.sql`.
5. To connect to the **News** database use command `psql news`


### Views created on DB*
##### *Very important please add the following views for the Tool to run correctly
**most_read**
Used to find most popular articles:
```SQL
  CREATE VIEW most_read AS
  SELECT articles.title,                                             
     count(log.path) AS views                                         
    FROM (articles                                                     
    JOIN log ON log.path = '/article/'|| articles.slug)
   GROUP BY articles.title                                            
   ORDER BY (count(log.path)) DESC                                    
  LIMIT 3;
 ```

 **total_views**
 Used to see each article view for author
```SQL
 CREATE VIEW total_views AS
 SELECT count(log.path) AS views,                                    
     articles.author                                                   
    FROM (articles                                                     
    JOIN log ON log.path = '/article/'|| articles.slug)
   GROUP BY articles.*, articles.author                               
   ORDER BY articles.author;
```

**popular_authors**
Used to find views by author

```SQL
CREATE VIEW popular_authors AS
  SELECT authors.name,                     
     sum(total_views.views) AS views       
    FROM total_views,                     
     authors                              
   WHERE (total_views.author = authors.id)
   GROUP BY authors.name                  
   ORDER BY views DESC;
 ```

**count_total**
Used to count total occurrences by day on log table.
```SQL
CREATE VIEW count_total AS
SELECT count(*) AS count,              
    time::date AS day    
   FROM log                                       
  GROUP BY day  
  ORDER BY day;
```

**count_fail**
Used to count the error occurrences by day on log table.
```SQL
CREATE VIEW count_fail AS
  SELECT count(log.status) AS fail,              
     time::date AS day  
    FROM log                                      
   WHERE (NOT (log.status = '200 OK'::text))      
   GROUP BY day  
   ORDER BY day;
```

**fail_and_total**
Displays fails and total occurrences by day from log table.
```SQL
CREATE VIEW fail_and_total AS
  SELECT count_fail.fail AS fail,         
     count_total.count AS total,           
     count_total.day                       
    FROM count_fail,                       
     count_total                            
   WHERE (count_fail.day = count_total.day)
   ORDER BY count_total.day;
```

**total_percentage**
Displays percentage of errors by day.
```SQL
CREATE VIEW total_percentage AS
 SELECT fail_and_total.day, round(((float8((fail_and_total.fail * 100)) / (fail_and_total.total)::double precision))::numeric, 1) AS percentage
    FROM fail_and_total;
```

**error_over_one**
Displays all days and percentage where the errors were over 1%
```SQL
CREATE VIEW error_over_one AS
  SELECT to_char(total_percentage.day, 'MON DD,YYYY'::text) AS to_char,
     total_percentage.percentage                                      
    FROM total_percentage
   WHERE (total_percentage.percentage > (1)::numeric);
```
"# Report-Tool" 

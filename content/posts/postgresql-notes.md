title: PostgreSQL Commands and SQL Examples for Data Science
slug: PostgreSQL for Data Science
category: database
date: 2017-11-04
modified: 2017-11-05

# PostgreSQL Commands and SQL Examples for Data Science
* **Debugging**
    * Finding all postgres processes:  `ps aux | grep postgres`
    * Finding process using a port: `lsof -i tcp:5432`
    * Finding process using a port: `netstat -vanp tÂcp | grep 5432`
    * Finding all running processes: `ps -A`
* **MacOS Installation and Configuration**
    * brew install postres
    * Login as admin user: `sudo -u user_name sql db_name`
    * Creating a db_user:  `CREATE ROLE user_name WITH LOGIN PASSWORD 'your secret here’;`
    * Changing persimmons: `ALTER ROLE user_name CREATEDB;`
    * Connecting to a server running as a regular user
        * pgAdmin > right-click server > Create > Sever
            * Main tab: Name it
            * Connection tab:  Specify IP address (e.g. 127.0.0.1)  > admin user / pw > role to operate as
* Invoke psql command shell
    - `psql -d <database> -U <user> -W <password>`
    - Note: Add `-E` to echo queries for learning


Command          | What it does
-----------------|--------------
`\l`             | List available databases
`\c <database>`  | Connect to a database
`\dt`            | List tables
`\dt *.*`        | List tables from all schemas
`\d <table>`     | Show table definition
`\dv`            | List views  
`\dn`            | List schemas  
`\df`            | List functions
`\df+ <function>`| Show SQL of function
`\h`             | psql help
`\? <psql cmd>`  | psql command help
`\h <sql>`       | SQL command syntax help
`\i <script>`    | Runs the SQL script file
`\q`             | Quit psql
`q`              | Quit current task and return to command line
`\x`             | Improves output formatting

* **Starting and Stopping the Server on MacOS**
        * `su - <admin_user>` # start and stop the server
        * `alias pgq='pg_ctl -D /usr/local/var/postgres stop -s -m fast'`
        * `alias pgs='pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start’`
    * Use `psql` to work with PostgreSQL on the command line or the `pgAdmin4` GUI application (available as a homebrew cask)
* **SQL Commands**
    * Creating
        * Database: Right-click on Databases > Create > Database
        * Tables:  
            * pgAdmin
                * Double-click on database > Double click on Schemes > Right-click on tables > Create
                * Columns:  Right-click on table > Create > Column > Give it a name > Give it a type
                * Constraint:  Right-click on table > Properties > Constraints tab > Add an constraint > Edit icon > Name it > Select Definition tab > Select column
            * Command
                ```sql
                CREATE TABLE animals
                (
                    species character varying (25),
                    vertebrate_class character varying(25),
                    appearance character varying(25),
                    num_legs int4,
                    CONSTRAINT animal_pkey PRIMARY KEY (species)
                );```
            * Import data
                * pgadmin: right-click table > Import / Export > Define location, delimiter, header … > OK
                * Check:
                    ```sql
                    SELECT *
                    FROM pets;```
    * **Statistics**
        * Limit number of results:
            ```sql
            SELECT *
            FROM staff
            LIMIT 10;```
        * Counting and grouping results
            ```sql
            SELECT gender, count(*)
            FROM staff
            GROUP BY gender;```
        * Finding the max and min
            ```sql
            SELECT max(salary), min(salary)
            FROM staff;```
        * Apply that across all departments:
            ```sql
            SELECT department, max(salary), min(salary)
            FROM staff
            GROUP BY department;```
        * Aggregate and round values  
            ```sql
            SELECT department, round(sum(salary), 0), round(avg(salary), 0), round(var_pop(salary), 0), round(stddev_pop(salary), 0)
            FROM staff
            GROUP BY department;```
        * Truncating, ceil and rounding
            ```sql
            SELECT department, avg(salary), trunc(avg(salary),2 ), ceil(avg(salary)), round(avg(salary), 2)  from staff
            GROUP BY department;```
    * Documentation: [PostrgreSQL Aggregation Functions](https://www.postgresql.org/docs/current/static/functions-aggregate.html)
    * **Classification**
        * Use CASE to show pet names and a column to indicate whether the pet's name is long or short (a long name is strictly more than 6 characters long). Filter to select only female pets.
            ```sql
            SELECT name ,
                CASE WHEN length(name) > 6
                THEN 'long'
                ELSE 'short' END  
            FROM pets
            WHERE gender = 'female';```
    * **Filtering**
        * Find data that meets a condition
            ```sql
            SELECT last_name, department, salary
            FROM staff
            WHERE salary > 100000;```
        * Adding multiple conditions to the WHERE clause
            ```sql
            SELECT last_name, department, salary
            FROM staff
            WHERE department = 'Tools' AND salary > 100000;```
        * Wild card in where clause
            ```sql
            SELECT last_name, department, salary
            FROM staff
            WHERE department
            LIKE 'B%’;```
        * Combining filters and aggregates
            ```sql
            SELECT department, sum(salary)
            FROM staff WHERE department
            LIKE 'B%'
            GROUP BY department;
            -- NOTE:  Slow queries result from putting ‘&’ first as scans every row ignoring the index```
        * Find distinct values
            ```sql
            SELECT DISTINCT LOWER(department)
            FROM staff;```
    * **Munging**
        * Concatenating values
            ```sql
            SELECT job_title || '-' || department
            FROM staff;```
        * … and create a new column
            ```sql
            SELECT job_title || '-' || department title_dept
            FROM staff;```
        * trim and length functions
            ```sql
            SELECT length(' software engineer '), length(trim(' software engineer ‘));  
            —-Results in: 19, 17```
        * Create new boolean field
            ```sql
            SELECT job_title, (job_title LIKE '%Assistant%') is_assist
            FROM staff;```
        * Extracting substring of length 3
            ```sql
            SELECT SUBSTRING('abcdefghijkl'
                FROM 6 FOR 3) test_string;
                —- Results: fgh;```
        * Extracting remainder of a string
            ```sql
            SELECT SUBSTRING('abcdefghijkl' FOR 4) test_string;
            —- Results: abcd;```
        * Replacing text
            ```sql
            SELECT OVERLAY(job_title PLACING 'Asst.'
            FROM 1 FOR 9)
            FROM staff
            WHERE job_title
            LIKE 'Assistant%’;```
    * **Regex**
        * Find assistants at specified levels
            ```sql
            SELECT job_title
            FROM staff
            WHERE job_title
            SIMILAR TO '%Assistant%(III|IV)’;```
        * … now match levels starting with I
            ```sql
            SELECT job_title
            FROM staff
            HERE job_title
            SIMILAR TO '%Assistant% I_’;```
        * … or job title that start with E, P or S  
            ```sql
            SELECT job_title
            FROM staff
            WHERE job_title
            SIMILAR TO '[EPS]%’;```
    * **Sub-Queries**
        * _Consider using a view and or a windowing functions for simpler, more readable code._
        * Adding a calculated field
            ```sql
            SELECT s1.last_name, s1.salary, s1.department,
                (SELECT round(avg(salary))
                FROM staff s2
                WHERE s2.department = s1.department )
            FROM staff s1;```
        * Using a sub-query instead of a table name
            ```sql
            SELECT s1.department, round(avg(s1.salary))
            FROM
                (SELECT department, salary
                FROM staff
                WHERE salary > 100000) s1
            GROUP BY department;```
            * using a sub-query to find max salary
            ```sql
            SELECT s1.department, s1.last_name, s1.salary
            FROM staff s1
            WHERE s1.salary = (SELECT max(s2.salary)
            FROM staff s2);```
        * Documentation:[PostgreSQL SubQuery Expressions](https://www.postgresql.org/docs/current/static/functions-subquery.html)
    * **Joining Tables**
        * Join two tables using department name
            ```sql
            SELECT s.last_name, s.department, cd.company_division
            FROM staff
            JOIN company_divisions cd
            ON s.department = cd.department;
                -- Note:  it is missing rows because not all departments
                -- in the staff table are found in the company_divisions table,
                -- so we need to prefer the division from the staff table.  
                -- This is called a left outer join.```
        * Left outer-join gets all rows
            ```sql
            SELECT s.last_name, s.department, cd.company_division
            FROM staff s
            LEFT JOIN company_divisions cd
            ON s.department = cd.department;```
        * … find departments without a division
            ```sql
            SELECT s.last_name, s.department, cd.company_division
            FROM staff s
            LEFT JOIN company_divisions cd
            ON s.department = cd.department
            WHERE cd.company_division IS NULL;
                -- Note:  Turns out it is the Books department```
    * **Using Views**
        * Save a long join by creating a view
            ```sql
            CREATE VIEW staff_div_reg AS
                SELECT s.*, cd.company_division, cr.company_regions
                FROM staff s
                LEFT JOIN company_divisions cd
                ON s.department = cd.department
                LEFT JOIN company_regions cr
                ON s.region_id = cr.region_id;```
        * Check that all rows are present in the view
            ```sql
            SELECT count(*)
            FROM staff_div_reg;```
        * Query to be stored as a view
            ```sql
            SELECT company_regions, count(*)
            FROM staff_div_reg  
            GROUP BY company_regions
            ORDER BY company_regions;```
        * Use view to provide counts of staff in each region
            ```sql
            CREATE OR REPLACE VIEW staff_div_reg_country
            AS
                SELECT s.*, cd.company_division, cr.company_regions, cr.country
                FROM staff s, company_divisions cd, company_regions cr;```
        *  Create a view that joins user and sales tables
            ```sql
            CREATE VIEW sales_by_person
            AS
                SELECT s.name, s.id, o.amount
                FROM salesperson s
                LEFT JOIN orders o
                ON s.id = o.salesperson_id;
                    -- Note: Every time the view is used
                    --       its SQL is re-evaluated.
                ```
        * Create a materialized view that is stored on the server
            ```sql
            CREATE MATERIALIZED VIEW sales_by_person
            AS
                SELECT s.name, s.id, o.amount
                FROM salesperson s
                LEFT JOIN orders o
                ON s.id = o.salesperson_id;
                    -- Note: Once created materialized views
                    --       can be queried many times but are
                    --       not automatically updated.
                ```
        * Updating a materialized view
            ```sql
            REFRESH MATERIALIZED VIEW sales_by_person;```
        * Report number and amount of successful sales by name
            ```sql
            SELECT name, count(amount), sum(amount)
            FROM sales_by_person
            GROUP BY name
            HAVING count(amount) > 1
            ORDER BY name;```
        * Documentation:
            - [PostgreSQL Views and the Rule System](https://www.postgresql.org/docs/current/static/rules-views.html)
            - [PostgreSQL Materialized Views](https://www.postgresql.org/docs/current/static/rules-materializedviews.html)
    * Temporary Tables
        * Temporary tables are alternative to Views and Subqueries
        * Here are two ways to create a temporary table in SQL
        *  Create and drop
            ```sql
            -- create a temporary table
            CREATE TABLE temp_table AS
            (
                SELECT col1, col2, col3
                FROM another_table;
            )

            -- select the data you need
            SELECT tt.col1, tt.col2
            FROM temp_table AS tt;

            -- delete the temporary table from the database
            DROP TABLE temp_table;
            ```
        * True temporary table created using WITH
            ```sql
            -- create the temporary table
            WITH temp_table AS
            (
                SELECT col1, col2, col3
                FROM another_table
            );

            -- select the data you need
            SELECT tt.col1, tt.col2
            FROM temp_table AS tt;
            ```
    * **Grouping & Totaling**
        * Breakout sales number and amount of sales by name
            ```sql
            SELECT s.name, count(o.amount), sum(o.amount)
            FROM salesperson s
            LEFT JOIN orders o
            ON s.id = o.salesperson_id
            GROUP BY s.name
            HAVING count(o.amount) > 1
            ORDER BY s.name;```
        *  Breakout the total number of employees by division and region using grouping set
             ```sql
            SELECT company_division, company_regions, count(*)
            FROM staff_div_reg
            GROUP BY GROUPING SETS (company_division, company_regions)
            ORDER BY company_regions, company_division;
                -- Note: Cells are blank when sub-totaled by another quantity```
        * Create subtotals using rollup
            ```sql
            SELECT company_regions, country, count(*)
            FROM staff_div_reg_country
            GROUP BY ROLLUP(country, company_regions)
            ORDER BY country, company_regions;```  
        * Create all possible subtotals using cube
            ```sql
            SELECT company_division, company_regions, count(*)
            FROM staff_div_reg_country
            GROUP BY CUBE(company_division, company_regions);```
        * Documentation: [PostgreSQL Grouping, Cube and Rollup](https://www.postgresql.org/docs/10/static/queries-table-expressions.html#queries-grouping-sets)
    * **Sorting / Ordering**
        * Find the top N values
            ```sql
            SELECT last_name, job_title, salary
            FROM staff
            ORDER BY salary DESC
            FETCH FIRST 10 ROWS ONLY;
                -- Note:  LIMIT get the first N elements, FETCH scans all
                --        the rows and get the highest N values.```
        * Ascending ordering by count
            ```sql
            SELECT company_division, count(*)
            FROM staff_div_reg_country
            GROUP BY company_division
            ORDER BY count(*);```
        * Descending order by count
            ```sql
            SELECT company_division, count(*)
            FROM staff_div_reg_country
            GROUP BY company_division
            ORDER BY count(*) DESC;```
        * Limit to first 3 rows
            ```sql
            SELECT company_division, count(*)
            FROM staff_div_reg_country GROUP BY company_division
            ORDER BY count(*) DESC
            FETCH FIRST 3 ROWS ONLY;```
        * Sorting by date
            ```sql
            SELECT facility_id, bed_census_date
            FROM beds
            WHERE facility_id = '6057'
            ORDER BY bed_census_date::timestamp ASC;```
        * Finding the largest totals by sorting an aggregated field
            ```sql
            SELECT facility_name, facility_id, bed_census_date, sum(available_residential_beds::integer)
            FROM beds
            GROUP BY facility_name, facility_id, bed_census_date
            ORDER BY sum(available_residential_beds::integer) DESC
            FETCH FIRST 10 ROWS ONLY;```
        * Documentation: [PostgreSQL Sorting Documentation](https://www.postgresql.org/docs/current/static/queries-order.html)
    * **Window Functions**
        * Window functions are simpler than subqueries and produce similar results
        * Operates on rows adjacent to the current row
            ```sql
            SELECT company_regions, last_name, salary, min(salary)
            OVER
                (
                    PARTITION BY company_regions
                )
            FROM staff_div_reg;```
        * Employees by department sorted by salary
            ```sql
            SELECT department, last_name, salary, first_value(salary)
            OVER
                (
                    PARTITION BY department
                    ORDER BY salary DESC
                )
            FROM staff;```
        * Employees by department sorted by last_name
            ```sql
            SELECT department, last_name, salary, first_value(salary)
            OVER
                (
                    PARTITION BY department
                    ORDER BY last_name
                )
            FROM staff;```
        * Ranking employees within a department by salary
            ```sql
            SELECT department, last_name, salary, rank()
            OVER
            (
                PARTITION BY department
                ORDER BY salary DESC
            )
            FROM staff;```
        * Lag function references previous row
            ```sql
            SELECT department, last_name, salary, lag(salary)
            OVER
                (
                    PARTITION BY department
                    ORDER BY salary DESC
                )
            FROM staff;```
        * Lead function references the next row
            ```sql
            SELECT department, last_name, salary, lead(salary)
            OVER
            (
                PARTITION BY department
                ORDER BY salary DESC
            )
            FROM staff;```
        * Calculating salary quartiles using ntile
            ```sql
            SELECT department, last_name, salary, ntile(4)
            OVER
            (
                PARTITION BY department
                ORDER BY salary DESC
            )
            FROM staff;```
        * Documentation: [PostgreSQL Windowing Function Expressions](https://www.postgresql.org/docs/current/static/functions-window.html)
* **Telling Stories with Data**
    * Start with a problem
        * Losing customers
        * Product sales decreasing
    * Gather data it will take time, figure in more time when using different data sources to make them all consistently encoded
    * Understand your data using statistics
    * Reformat and check it before attempting to do joins
    * Use views to capture complex SQL statements
    * Use joins
        * Inner joins only return row that both table share
        * Use an outer join if you want all rows from one table even if they are missing from the other table
    * For cross tabulations use cubes, rollups, and grouping sets rather than subqueries
    * Use window functions to work on sets of related rows
* **Resources**
    * Tutorial: [https://www.tutorialspoint.com/postgresql/index.htm](https://www.tutorialspoint.com/postgresql/index.htm)
    * Tutorial: [http://www.postgresqltutorial.com/(http://www.postgresqltutorial.com/)]
    * PostrgreSQL Aggregation Functions: [https://www.postgresql.org/docs/current/static/functions-aggregate.html](https://www.postgresql.org/docs/current/static/functions-aggregate.html)
    * Joins explained visually: [https://www.codeproject.com/Articles/33052/Visual-Representation-of-SQL-Joins](https://www.codeproject.com/Articles/33052/Visual-Representation-of-SQL-Joins)
    * SQL for Data Science from Lynda.com: [https://www.lynda.com/SQL-tutorials/SQL-Tips-Tricks-Data-Science/558576-2.html](https://www.lynda.com/SQL-tutorials/SQL-Tips-Tricks-Data-Science/558576-2.html).  I highly recommend this course. Increasingly Lynda.com's excellent courses are available through your local library.  Library patrons in Denver can access this course through [Denver Public Library Teach Yourself Technology page]()
    * SQL for Data Science from Lynda.com: [https://www.lynda.com/SQL-tutorials/SQL-Tips-Tricks-Data-Science/558576-2.html](https://www.lynda.com/SQL-tutorials/SQL-Tips-Tricks-Data-Science/558576-2.html). This is an excellent course and increasingly Lynda's courses are available through your local library.  Here in Denver library patrons can access all of Lynda's courses through the [Denver Public Library Teach Yourself Technology page](https://www.denverlibrary.org/teach-yourself-technology).

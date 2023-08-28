# University-Professor-Search-Engine

## Purpose
This application has been designed with the purpose of assisting prospective university students in their search for information related to universities, faculties, publications, and various search topics. The primary target users for this application are students who are in the process of deciding on the professors they would like to study from in university. The application features a user-friendly dashboard interface that allows students to easily query information and view research results related to the provided input keywords.

## Installation
The installation is described below

Step 1: Download and access databases: MySql, Neo4j, and MongoDB databases should be downloaded and ready to be used.

Step 2:  Install python libraries:
“pip3 install dash
pip3 install pandas
pip3 install plotly
pip3 install neo4j”

Step 3. To run the application, use the following command in the command-line interface (CLI) while located in the root folder of the project:
“python3 app.py mysql_db.py  mongo_db.py neo4j_db.py”
This command will execute the app.py file and launch the application.


## Design & Usage
Our team has researched various academic keywords comprehensively and developed seven efficient widgets for the UniversityProfessorSearchEngine. These widgets are purposefully tailored to meet the requirements of prospective university students, allowing them to easily access and analyze data relevant to their areas of interest.

### widget 1 Top N Keywords (neo4j)
This scatter plot analyzes the frequency of the top keywords across different research topics (e.g. internet, power control, etc.), aiding in identifying the most popular areas of research. By using this information, students can make well-informed decisions when choosing their potential major of study at the university.

●	How to use it:
A slider has been incorporated into the design, allowing users to select a number from 5 to 20 (N value), which determines the display of the top N keywords with their frequency. Users can adjust the slider by manually dragging it to their preferred value of N. Consequently, the "Top N Keywords" graph will dynamically update based on the users' selected value.

### widget 2 Top Cited Publications (MongoDB)
This table serves to display the top publication according to the cited frequency and aids in the identification of the most popular areas of research. The purpose of this graph is to assist students in selecting the study topics they would like to work on in the future based on the citation records.


### widget 3 Top 5 Keywords per School (MySQL)
This widget is designed to search for the top 5 keywords commonly used across various topics at different schools. By doing so, users can identify each university's primary study areas of focus.

●	How to use it:
Users can enter the university name and click the Search button to search the information related to a specific university. This input feature allows users to input the name of the university they want to explore. After the Search button is clicked, the application initiates the search and retrieves the top 5 keywords associated with the input university. The output is presented in the form of a pie chart, which shows the percentage of the top 5 keywords among all keywords associated with the specific university. This pie chart highlights the trending areas of study at the selected university and provides visualizations of the university's academic focus.

### widget 4 Most cited publications per school (MySQL)
This widget allows users to query and retrieve the top 5 most cited publications within a particular university. The rankings are determined based on the number of citations accumulated by each publication.

●	How to use it:
Users can input the names of different universities they want to search and compare. The application allows for the input of multiple university names. Upon submitting the information, the output is presented as a bar chart, displaying the total citation counts of the top 5 most cited publications for input universities. The bar chart can provide information for users to quickly compare the focus of each university.

### widget Top 5 Faculty search engine (MySQL)
This widget is designed to search for and display the top 5 faculty members who are related to one keyword within a specified university. It is utilized to fetch the publication count of professors at a specific university. By accessing this information, students can use this information and make informed decisions to enroll in classes taught by the most interesting professors. The purpose of this widget is to assist students in selecting the professors they would like to work with in the future based on the professors' research impact and citation records.

●	How to use it:
Users can input the University Name and the Keyword to search the faculty members from a specific university based on a particular keyword. The University Name input feature enables users to filter faculty members based on their affiliation with the chosen university. And the Keyword input allows users to filter faculty members based on the specified keyword and further narrow down faculty search based on research interests. The output is presented as a faculty bar chart, displaying the top 5 faculty members with the highest publication count score. The bar chart provides a clear visual representation of the faculty members whose research aligns with the given keyword, contributing to the objective of aiding users in identifying faculty members with expertise in specific research areas.

Faculty Information Search
### widget 6.1 Photo & Contact Information (MongoDB)
This widget is used to present the photo and contact information of a selected faculty member who specializes in a school. By using this widget, students can easily view the photo of the professor they are interested in and access their contact details for further communication or inquiries.
### widget 6.2 Top 5 keywords for this faculty (MySQL)
This widget presents the top 5 keywords related to the selected faculty member. Students can get more information about the professor's research area using this widget.

●	How to use it:
Users can input the University Name and the Faculty Name to search for faculty members from a specific university. The University Name input feature enables users to filter faculty members based on their affiliation with the input university. The Faculty Name input allows users to search for faculty information found on the specified name, supporting the objective of narrowing down faculty search by individual faculty members. The output of widget 6.1 presents the faculty member's photo and relevant information, such as the position, phone, and Email. The output of widget 6.2 is a pie chart that illustrates the professor's area of focus in their studies. This comprehensive information contributes to the objective of providing users with a comprehensive overview of the faculty members they are searching for, facilitating further communication or inquiries.

### widget 7 My Favorite Professor (MySQL)
This widget is used to assist users in organizing their list of preferred faculty members. After the previous search steps (from widget 1 to widget 6), users can gain insights into their preferred school and favorite faculty members. And then, they can add their names to a list for future reference.

●	How to use it:
Users can click the Add or Remove button to manage their list of saved favorite faculty members. By clicking the Add button, users can add a preferred faculty member to their list, which allows them to save their favorite faculty for future reference. Additionally, clicking the Remove button enables users to remove a faculty from their list, which allows users to manage their saved favorite faculty. The output displays a list table of faculty names, presenting users with a comprehensive view of their saved favorite faculty. The list table enhances the user experience by offering a convenient and organized way to access and review their preferred faculty members.


## Implementation:
This application is engaged in both frontend and backend development.
Frontend:
We utilized the Dash framework and other crucial libraries like Pandas, dash_bootstrap_components, and Dash Plotly during the frontend development. Three objects of the connection classes - MySqlConnector, MongoConnector and Neo4jConnector were initialized to establish database connections. In addition, seven callback functions were defined, and they used objects to call the corresponding query functions defined within the connection classes. This approach ensures efficient data retrieval and updating based on users' input keywords, enhancing the application's overall user experience and functionality.
Backend:
Databases are stored in MySQL, Neo4j, and MongoDB.
- SQL connection class: Pandas and sqlalchemy are used to interact with MySQL database using the MySQL language. These libraries facilitate seamless data manipulation and communication with the MySQL database, enabling efficient querying and processing of data within the application.
- Neo4j connection class: Pandas and neo4j are used to interact with Neo4j database using the Neo4j language. These libraries improved data retrieval and visualization capabilities within the application.
- MongoDB connection class: Pandas and pymongo are essential libraries employed in the application to interact with the MangoDB database using the MangoDB language. These libraries ensure effective integration and utilization of the MongoDB database and enable smooth querying and data management processes within the application.


## Database Techniques:
In this application, we have integrated several essential database techniques to enhance the efficiency of database queries, including indexing, view, constraint, and procedure.

1. 	Indexing
We have created an index on the university,  keyword and faculty table to support queries widget5 and widget7. This indexing function is defined in the SQL connection class. Indexing plays an important role in achieving the fastest response times for frequently executed queries. By creating indexes on one or more columns, we can have rapid random lookups and efficient ordering of access to records. Executing the same query without an index would require inspecting every row in the table to retrieve the required data. In conclusion, indexing provides a shortcut and significantly reduces query times, especially on large tables.

      ```
      DROP PROCEDURE IF EXISTS create_index

      CREATE PROCEDURE create_index()
                BEGIN
                    DECLARE index_exists INT;
                    SELECT COUNT(*)
                    INTO index_exists
                    FROM information_schema.statistics
                    WHERE table_schema = '{database_name}'
                      AND table_name = '{table_name}'
                      AND index_name = '{index_name}';
                    IF index_exists = 0 THEN
                        SET @create_index_sql = CONCAT('CREATE INDEX ', '{index_name}', ' ON ', '{table_name}', ' (', '{column_name}', ')');
                        PREPARE stmt FROM @create_index_sql;
                        EXECUTE stmt;
                        DEALLOCATE PREPARE stmt;
                    END IF;
                END
       ```

2. 	View
We have created a view on faculty-keyword-university in the SQL database to support queries in widget 3. The code is shown below, and the function is defined in the SQL connection class. A view is a virtual table that is derived from one or more underlying tables but is not physically stored in the database. Instead, it provides a simplified and consolidated representation of the data from these three tables. By doing this, we can avoid joining the "keyword" and "university" tables and directly access the data required from the view. This approach can improve the query's performance, as the pre-computed view is accessed instead of joining the tables at runtime. Besides that, using the view makes querying and analyzing the data easier and faster.

     ```
       DROP VIEW IF EXISTS keyword_university_view

       CREATE VIEW keyword_university_view AS
                SELECT university.name AS school, keyword.name AS keyword, keyword.id AS kid
                FROM university, faculty, faculty_keyword, keyword
                WHERE university.id=faculty.university_id
                    AND keyword.id=faculty_keyword.keyword_id
                    AND faculty.id=faculty_keyword.faculty_id;
     ```
3.  Constraint
We have implemented constraints to enforce rules that ensure the integrity of the data. In the context of our application widget 7 allows users to add or remove favorite professors. However, we have set specific constraints to ensure data consistency and prevent invalid entries. For example, both the name and favorite fields must be provided and cannot be left empty or NULL. Additionally, we enforce a uni_pro_key constraint, which ensures that each professor can only be added once as a favorite. If a user attempts to add the same professor twice, the application will raise an error to maintain data integrity. These constraints help us maintain a reliable and accurate database for our users.

    ```
        CREATE TABLE favorite_prof (
             id INT AUTO_INCREMENT PRIMARY KEY,
             name VARCHAR(255) NOT NULL,
             favorited BOOLEAN NOT NULL DEFAULT FALSE,
             CONSTRAINT uni_pro_key UNIQUE (name, favorited)
        )
    ```

4. 	Stored procedure
We have created an "check_valid_prof" stored procedure in the MySQL database to ensure that only valid professor names are added to the list when interacting with Widget 7. This procedure serves the purpose of validating user input, and if the provided professor name does not exist in the university, it triggers an error. A stored procedure is a collection of SQL statements that are given a name and stored in a relational database management system. These procedures can be called by client applications, providing a more modular and reusable approach to executing SQL queries. Additionally, stored procedures offer performance benefits as they are compiled once and stored in the server's memory, resulting in faster execution. This stored procedure enhances the system's overall efficiency and promotes better database management.

```
DROP PROCEDURE IF EXISTS check_valid_prof

CREATE PROCEDURE check_valid_prof(IN professor_name VARCHAR(255), IN university_name VARCHAR(255), OUT is_valid BOOLEAN)
                BEGIN
                    DECLARE professor_count INT;

                    -- Check if the professor exists at the given university
                    SELECT COUNT(*) INTO professor_count
                    FROM faculty f, university u
                    WHERE f.university_id = u.id
                        AND u.name = university_name
                        AND f.name = professor_name;

                    -- Set the is_valid output parameter based on the professor count
                    SET is_valid = (professor_count > 0);
                END;
```

import pandas as pd
from sqlalchemy import create_engine

#TABLE_NAME = "FacultyAttribute"
DB_NAME = "academicworld"

class MySqlConnector:
    def __init__(self):
        connection_string = "mysql+mysqlconnector://root:qiu19900612@localhost:3306"
        self.engine = create_engine(connection_string) # connect to server
        self.engine.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        self.engine = create_engine(connection_string + f"/{DB_NAME}", echo=True)

    # create view
    def Create_view(self):
        with self.engine.begin() as conn:
            conn.execute("DROP VIEW IF EXISTS keyword_university_view")
            conn.execute("""
                CREATE VIEW keyword_university_view AS
                SELECT university.name AS school, keyword.name AS keyword, keyword.id AS kid
                FROM university, faculty, faculty_keyword, keyword
                WHERE university.id=faculty.university_id
                    AND keyword.id=faculty_keyword.keyword_id
                    AND faculty.id=faculty_keyword.faculty_id;
            """)


    # create index
    def IndexCreate(self, index_name, table_name, column_name, database_name):
        with self.engine.begin() as conn:
            conn.execute("DROP PROCEDURE IF EXISTS create_index")
            conn.execute(
                     f"""
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
            """
            )
            conn.execute("CALL create_index()")

    # create a favorite_prof table
    def CreateFavoriteProf(self):
        with self.engine.begin() as conn:
            conn.execute("DROP TABLE IF EXISTS favorite_prof")
            conn.execute("""
                CREATE TABLE favorite_prof (
                     id INT AUTO_INCREMENT PRIMARY KEY,
                     name VARCHAR(255) NOT NULL,
                     favorited BOOLEAN NOT NULL DEFAULT FALSE,
                     CONSTRAINT uni_pro_key UNIQUE (name, favorited)
                )
            """)

    # check the valid prof
    def CheckValidProf(self):
        with self.engine.begin() as conn:
            conn.execute("DROP PROCEDURE IF EXISTS check_valid_prof")
            conn.execute("""
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
            """
        )

    # # widget 1: Top N kewords
    def QueryTopKeyword(self, num):
        with self.engine.begin() as conn:
            result = conn.execute("SELECT k.name AS name, COUNT(k.id) AS count " + \
                                    "FROM keyword k, publication_keyword pk " + \
                                    "WHERE k.id = pk.keyword_id " + \
                                    f"GROUP BY k.id ORDER BY count DESC LIMIT {num};")
            res_key = pd.DataFrame(result, columns=["name", "count"])
            conn.close()
            return res_key

    # widget 3: Top 5 keywords per school
    def Query_top_keyword(self, university_name):
        with self.engine.begin() as conn:
            # result = conn.execute(f"SELECT keyword, COUNT(kid) AS count FROM myview WHERE school IN ('Stanford university') GROUP BY kid ORDER BY count DESC LIMIT 5;")
            result = conn.execute(f"SELECT keyword, COUNT(kid) AS count FROM keyword_university_view WHERE school = '{university_name}' GROUP BY keyword ORDER BY count DESC LIMIT 5;")
            res_key = pd.DataFrame(result, columns=["keyword", "count"])
            conn.close()
            return res_key

    # widget 3: get university.photo_url
    def Query_uni_photo(self, university_name):
        with self.engine.begin() as conn:
            result = conn.execute(f"SELECT name, photo_url FROM university WHERE name = '{university_name}';")
            res_photo = pd.DataFrame(result, columns=["name", "photo_url"])
            conn.close()
            return res_photo


    # widget 4: Most cited publications per school
    def QueryTopPublications(self, university_name):
        with self.engine.begin() as conn:
            result = conn.execute("SELECT title, University, total_citation " + \
                                    "FROM (SELECT p.title, u.name AS University, SUM(p.num_citations) AS total_citation, ROW_NUMBER() OVER (PARTITION BY u.name ORDER BY SUM(p.num_citations) DESC) AS row_num " + \
                                    "FROM faculty f JOIN university u ON f.university_id = u.id " + \
                                    "JOIN faculty_publication fp ON f.id = fp.faculty_id " + \
                                    "JOIN publication p ON fp.publication_id = p.id " + \
                                    f"WHERE u.name IN ({university_name})GROUP BY p.title, u.name) AS top_publications " + \
                                    "WHERE row_num <= 5;")

            res_pub = pd.DataFrame(result, columns=['title', 'university', 'total_citation'])
            conn.close()
        return res_pub

    # widget 5: Top five Faculty
    def QueryTopfauclty(self, university_name, keyword):
        with self.engine.begin() as conn:
            result = conn.execute("SELECT f.name AS name, SUM(pk.score*p.num_citations) AS score " + \
                                  "FROM faculty f JOIN faculty_publication fp ON f.id = fp.faculty_id " + \
                                  "JOIN publication p ON fp.publication_id = p.id " + \
                                  "JOIN publication_keyword pk ON p.id = pk.publication_id " + \
                                  "JOIN keyword k ON pk.keyword_id = k.id " + \
                                  "JOIN university u ON f.university_id = u.id " + \
                                  f"WHERE k.name = '{keyword}' AND u.name = '{university_name}' " + \
                                  "GROUP BY f.id ORDER BY score DESC LIMIT 5;")
            res_pub = pd.DataFrame(result, columns=['name', 'score'])
            conn.close()
        return res_pub

    # widget 6.1: Faculty Information Search
    def QueryFacultyTable(self, university_name, faculty_name):
        with self.engine.begin() as conn:
            result = conn.execute("SELECT f.name AS name, f.position AS position, u.name AS university, f.email AS email, f.phone AS phone, f.photo_url AS photo_urls " + \
                                  f"FROM faculty f, university u WHERE f.name = '{faculty_name}' AND u.name = '{university_name}'")
            res_prof_information = pd.DataFrame(result, columns=['name', 'position', 'university', 'email', 'phone','photo_url'])

            conn.close()
        return res_prof_information

    # widget 6.2: get Faculty top 10 keywords
    def QueryFacultyKeyword(self, university_name, faculty_name):
        with self.engine.begin() as conn:
            result = conn.execute(f"SELECT k.name AS keyword_name, SUM(fk.score) AS total_score FROM faculty f JOIN faculty_keyword fk ON f.id = fk.faculty_id JOIN keyword k ON fk.keyword_id = k.id JOIN university u ON f.university_id = u.id WHERE f.name = '{faculty_name}' AND u.name = '{university_name}' GROUP BY k.name ORDER BY total_score DESC LIMIT 5;")
            res_prof_information = pd.DataFrame(result, columns=['keyword_name', 'total_score'])
            conn.close()
        return res_prof_information

    # widget 7.1: add favorite professors
    def AddProf(self, faculty_name, is_favorite):
        with self.engine.begin() as conn:
            result = conn.execute(f"INSERT INTO favorite_prof (name, favorited) VALUES ('{faculty_name}', {is_favorite})")

    # widget 7.2: remove favorite professors
    def RemoveProf(self, faculty_name):
        with self.engine.begin() as conn:
            result = conn.execute(f"DELETE FROM favorite_prof WHERE name = '{faculty_name}'")

    # widget 7.3: get name from favorite_prof
    def get_favorite_prof(self):
        with self.engine.begin() as conn:
            result = conn.execute("SELECT name FROM favorite_prof")
            res_prof = pd.DataFrame(result, columns=["name"])
            conn.close()
            return res_prof

    def Close(self):
        self.engine.dispose()


#if __name__ == "__main__":
#    sql_db = MySqlConnector()
    #sql_db.InitializeDB()
#    top_keywords_df = sql_db.QueryFacultyTable('Craig Zilles')
#    top_keywords_df = sql_db.QueryTopKeyword()
#    print(top_keywords_df)
#    sql_db.Close()

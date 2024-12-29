import sqlite3
import pandas as pd


''' Create DBStorage() class to handle all interactions with database '''
class DBStorage():

    ''' Create database connection   '''
    def __init__(self):
        self.con = sqlite3.connect("links.db")
        self.setup_tables()

    ''' Define setup_tables() function to create db tables '''
    def setup_tables(self):
        ''' create cursor to run db queries '''
        cur = self.con.cursor()

        ''' create table '''
        results_table = r"""
            CREATE TABLE IF NOT EXISTS results (
                 id INTEGER PRIMARY KEY,
                 query TEXT,
                 rank INTEGER,
                 link TEXT,
                 title TEXT,
                 snippet TEXT,
                 html TEXT,
                 created DATETIME,
                 relevance INTEGER,
                 UNIQUE(query, link)
            );
        """

        ''' SQL Code Explanation

            1. CREATE TABLE IF NOT EXISTS

                This clause creates a new table in the database.
                IF NOT EXISTS ensures that the table is only created if it doesn't already exist, preventing errors from duplicate table creation.

            2. results

                The name of the table being created is results.

            3. Columns in the Table

            Each column is defined by its name, data type, and any additional constraints.

                id INTEGER PRIMARY KEY:
                    id is the primary key for the table, ensuring every row has a unique identifier.

                query TEXT:
                    Stores a search query as text.

                rank INTEGER:
                    Represents the ranking of a search result 

                link TEXT:
                    Stores the URL or hyperlink for the result.

                title TEXT:
                    Stores the title of the search result.

                snippet TEXT:
                    Stores a short snippet or summary of the result.

                html TEXT:
                    Stores the raw HTML content of the result.

                created DATETIME:
                    Records the date and time the result was created.

                relevance INTEGER:
                    Stores an integer representing the relevance of the result (for ranking or scoring).

            4. Constraints

                UNIQUE(query, link):
                    Ensures that no two rows have the same combination of query and link, preventing duplicate entries for a given query and link.
        
        '''

        ''' Run SQL''' 
        cur.execute(results_table)

        ''' Commit changes to db'''
        self.con.commit()

        ''' Close connection cursor '''
        cur.close()



    ''' Define query_results() takes query & returns all results from db '''
    def query_results(self, query):
         
         ''' Run SQL query against db '''
         df = pd.read_sql(f"select * from results where query='{query}' order by rank asc;", self.con)

         ''' Return dataframe '''
         return df


    ''' Define insert_row() to store results to db '''
    def insert_row(self, values):

        cur = self.con.cursor()

        try:
            cur.execute('INSERT INTO results (query, rank, link, title, snippet, html, created) VALUES(?,?,?,?,?,?,?)', values)

            ''' Execute the SQL Insert Command:
                The SQL command inserts data into the results table.
                    Column names: Specifies which columns to insert into.
                    Placeholders (?): Prevent SQL injection by parameterizing inputs.

                values: Contains the actual data to be inserted, matching the column order:
                    query, rank, title, snippet, html, created.
            
            
            '''

            self.con.commit()

        except sqlite3.IntegrityError:
            pass

            ''' Handle Unique Constraints:
                Catches any sqlite3.IntegrityError that occurs if the UNIQUE(query, link) constraint is violated.
                In such cases, the function silently ignores the error and does not insert the row.
                This prevents duplicate entries for the same combination of query and link.
        '''

        cur.close()

    # Update relevance of a specific result in the database
    def update_relevance(self, query, link, relevance):
        cur = self.con.cursor()
        # Executes an SQL UPDATE query to 
        # modify the relevance column for the matching query and link.
        cur.execute("UPDATE results SET relevance =? WHERE query=? AND link=?", [relevance, query, link])
        self.con.commit()
        cur.close()
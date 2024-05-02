
import os
from dotenv import load_dotenv
import pyodbc
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq


def connect_to_sql_server(server: str, database: str, username: str, password: str):
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        return conn
    except pyodbc.Error as e:
        print(f"Error connecting to SQL Server: {e}")
        return None 

def get_database_name(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT DB_NAME()")
        row = cursor.fetchone()
        return row[0]
    except pyodbc.Error as e:
        print(f"Error fetching database name: {e}")
        return None

# Provide your SQL Server credentials
server = 'DESKTOP-5QSJM94\\SQLEXPRESS'
database = 'AdventureWorksDW'
username = 'garima'
password = 'Welcome@123'

# Connect to SQL Server
conn = connect_to_sql_server(server, database, username, password)
if conn:
    try:
        # Get the database name
        db_name = get_database_name(conn)
        if db_name:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES")
            tables = cursor.fetchall()
            print(tables)  # Or perform any other operations with the table information
        else:
            print("Failed to fetch database name.")
    except pyodbc.Error as e:
        print(f"Error executing SQL query: {e}")
    finally:
        conn.close()
else:
    print("Failed to connect to SQL Server.")


#2nd part

template = """Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
SQL Query:"""
prompt = ChatPromptTemplate.from_template(template)

# 3rd part
def get_schema(tables):
    schema = tables.get_table_info()
    return schema

#4th part

#load_dotenv()
#groq_api_key=os.environ['GROQ_API_KEY']


llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0,groq_api_key='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')

sql_chain = (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt
    | llm
    | StrOutputParser()
)
 
#5th part

user_question = 'how many albums are there in the database?'
sql_chain.invoke({"question": user_question})

# 'SELECT COUNT(*) AS TotalAlbums\nFROM Album;'

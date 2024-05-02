
import os
from dotenv import load_dotenv
import pyodbc
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import pymssql



#db_uri = "mssql+pymssql://garima:Welcome@123@DESKTOP-5QSJM94/AdventureWorksDW"
db_uri= "mssql+pyodbc://garima:hello123@DESKTOP-5QSJM94\SQLEXPRESS:1433/test?driver=ODBC+Driver+17+for+SQL+Server"

db=SQLDatabase.from_uri(db_uri)
  

#2nd part

template = """Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
SQL Query:"""
prompt = ChatPromptTemplate.from_template(template)

# 3rd part
def get_schema(_):
    return db.get_table_info()

#4th part

#load_dotenv()
#groq_api_key=os.environ['GROQ_API_KEY']


llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0, groq_api_key='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')

sql_chain = (
    RunnablePassthrough.assign(schema=get_schema)
    | prompt
    | llm
    | StrOutputParser()
)
 
#5th part

user_question = 'how many distinct cities are there?'
sql_chain.invoke({"question": user_question})

# 'SELECT COUNT(*) AS TotalAlbums\nFROM Album;'

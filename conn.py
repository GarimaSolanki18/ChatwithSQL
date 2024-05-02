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



db_uri= "mssql+pyodbc://garima:hello123@DESKTOP-5QSJM94\SQLEXPRESS:1433/AdventureWorksDW?driver=ODBC+Driver+17+for+SQL+Server"

db=SQLDatabase.from_uri(db_uri)
print(db.get_table_info())

def get_schema(db):
    return db.get_table_info()


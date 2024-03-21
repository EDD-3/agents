# File that contains SQL related "tools"
import sqlite3
from typing import List

from langchain.tools import Tool
from pydantic.v1 import BaseModel

conn = sqlite3.connect("db.sqlite")


def join_row_info_in_chatgpt_readable_form(rows):
    return


# Function that grabs table names from the sqlite db, it is used in a system message for the agent
def list_tables():
    """Function that list the name of tables in a sqlite database"""
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return "\n".join(row[0] for row in rows if row[0] is not None)


def run_sqlite_query(query):
    """Function that runs a sql query created by a langchain Agent"""
    c = conn.cursor()
    try:
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as err:
        return f"The following error occured: {str(err)}"


class RunQueryArgsSchema(BaseModel):
    query: str


run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a sqlite query.",
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema,
)


def describe_tables(table_names):
    """Function that describes the name of columns of tables in a database"""
    c = conn.cursor()
    tables = ", ".join("'" + table + "'" for table in table_names)
    rows = c.execute(
        f"SELECT sql FROM sqlite_master WHERE type='table' and NAME IN ({tables});"
    )
    return "\n".join(row[0] for row in rows if row[0] is not None)


class DescribeTablesArgsSchema(BaseModel):
    table_names: List[str]


describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, returns the schema",
    func=describe_tables,
    args_schema=DescribeTablesArgsSchema,
)

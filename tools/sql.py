# File that contains SQL related "tools"
import sqlite3

from langchain.tools import Tool

conn = sqlite3.connect("db.sqlite")


def join_row_info_in_chatgpt_readable_form(rows):
    return "\n".join(row[0] for row in rows if row[0] is not None)


# Function that grabs table names from the sqlite db, it is used in a system message for the agent
def list_tables():
    """Function that list the name of tables in a sqlite database"""
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return join_row_info_in_chatgpt_readable_form(rows=rows)


def run_sqlite_query(query):
    """Function that runs a sql query created by a langchain Agent"""
    c = conn.cursor()
    try:
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as err:
        return f"The following error occured: {str(err)}"


run_query_tool = Tool.from_function(
    name="run_sqlite_query", description="Run a sqlite query.", func=run_sqlite_query
)


#
def describe_tables(table_names):
    """Function that describes the name of columns of tables in a database"""
    c = conn.cursor()
    tables = ", ".join("'" + table + "'" for table in table_names)
    rows = c.execute(
        f"SELECT sql FROM sqlite_master WHERE type='table' and NAME IN ({tables});"
    )
    return join_row_info_in_chatgpt_readable_form(rows=rows)


describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, returns the schema",
    func=describe_tables,
)

import pandas as pd

from config import sqliteConfig


def tbl_fun_View():
    # Get connections and cursors from your SQLite config
    cursorRead, cursorWrite, engineConRead, engineConWrite, conn = sqliteConfig.sqlite()
    
    # Define your query
    query = "SELECT * FROM Functions"
    
    # Execute the query and return the result as a DataFrame
    df = pd.read_sql_query(query, engineConRead)
      
    return df


def relative_tbl_data():
    cursorRead, cursorWrite, engineConRead, engineConWrite, conn = sqliteConfig.sqlite()
    
    # Define your query
    query = "SELECT id, FunctionId, Objects, DefaultValues, WorksheetColumnName FROM Function_Data"
    
    # Execute the query and return the result as a DataFrame
    df = pd.read_sql_query(query, engineConRead)
    df.columns = ["Id", "FunctionId", "Objects", "DefaultValues", "WorksheetColumnName"]
    return df



def reverse_lookup(dictionary, target_value):
        for key, value in dictionary.items():
            if value == target_value:
                return key
        return None  # Return None if the value is not found in the dictionary
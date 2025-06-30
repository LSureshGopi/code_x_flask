import pandas as pd
from modules import logs 
from config import sqliteConfig

def edit_fun_tbl(id, fun, fundec):
    # Get connections and cursors from your SQLite config
    cursorRead, cursorWrite, engineConRead, engineConWrite, conn = sqliteConfig.sqlite()
    
    try:
        update_query = """
            UPDATE Functions 
            SET FunctionName = ?, FunctionDescription = ? 
            WHERE Id = ?
        """
        cursorWrite.execute(update_query, (fun, fundec, id))
        conn.commit()
        logs.log_user_activity("Updated Data on table Functions")
        return True  # Update successful
    except Exception as e:
        print(f"Error updating Function: {e}")
        return False  # Update failed
    
def delete_fun_tbl(id):
    cursorRead, cursorWrite, engineConRead, engineConWrite, conn = sqliteConfig.sqlite()

    try:
        delete_query = "DELETE FROM Functions WHERE Id = ?"
        cursorWrite.execute(delete_query, (id,))
        conn.commit()

        logs.log_user_activity("Deleted Data on table Functions")
        return True
    except Exception as e:
        print(f"Error deleting Function with ID {id}: {e}")
        return False
    
def insert_fun_tbl(fun, fundec):
    cursorRead, cursorWrite, engineConRead, engineConWrite, conn = sqliteConfig.sqlite()

    try:
        insert_query = "INSERT INTO Functions (FunctionName, FunctionDescription) VALUES (?, ?)"
        cursorWrite.execute(insert_query, (fun, fundec))
        conn.commit()
        logs.log_user_activity("Inserted Data on table Functions")
        return True
    except Exception as e:
        print(f"Error inserting new function: {e}")
        return False

def edit_fundata_tbl(id, function_id, object, defValue, worksheetName):
    # Get connections and cursors from your SQLite config
    cursorRead, cursorWrite, engineConRead, engineConWrite, conn = sqliteConfig.sqlite()
    
    try:
        update_query = """
            UPDATE Function_Data 
            SET FunctionId = ?, Objects = ?, DefaultValues = ?, WorksheetColumnName = ?
            WHERE id = ?
        """
        cursorWrite.execute(update_query, (function_id, object, defValue, worksheetName, id))
        conn.commit()
        logs.log_user_activity("Updated Data on table Functions View")
        return True  # Update successful
    except Exception as e:
        print(f"Error updating Function: {e}")
        return False  # Update failed
    
def delete_fundata_tbl(id):
    cursorRead, cursorWrite, engineConRead, engineConWrite, conn = sqliteConfig.sqlite()

    try:
        delete_query = "DELETE FROM Function_Data WHERE id = ?"
        cursorWrite.execute(delete_query, (id,))
        conn.commit()
        logs.log_user_activity("Deleted Data on table Functions View")
        return True
    except Exception as e:
        print(f"Error deleting Function_Data with ID {id}: {e}")
        return False
    
def insert_fundata_tbl(function_id, object, defValue, worksheetName):
    cursorRead, cursorWrite, engineConRead, engineConWrite, conn = sqliteConfig.sqlite()

    try:
        insert_query = "INSERT INTO Function_Data (FunctionId, Objects, DefaultValues, WorksheetColumnName) VALUES (?, ?, ?, ?)"
        cursorWrite.execute(insert_query, (function_id, object, defValue, worksheetName))
        conn.commit()
        logs.log_user_activity("Inserted Data on table Functions View")
        return True
    except Exception as e:
        print(f"Error inserting new function: {e}")
        return False
    




    
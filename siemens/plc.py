import pandas as pd
from config import sqliteConfig
from modules import main
from modules import logs
from model.siemens.tia_code import app_generate_cm_db, app_generate_CM_fb
from model.siemens.tia_textlists import app_plc_textlists

# ---------- Export Function Block (FB) ----------
def _exportLogixRungsSie(nr, selection_module, df):
    if not nr:
        return {"status": "error", "message": "Please enter PLC NR."}

    try:
        cursor_read, cursor_write, engine_read, engine_write, conn = sqliteConfig.sqlite()

        cursor_read.execute("SELECT * FROM Functions")
        column_data = cursor_read.fetchall()
        col_data = {
            row[0]: row[1] if len(row) >= 2 else "UNKNOWN"
            for row in column_data
        }

        fun_id = main.reverse_lookup(col_data, selection_module)

        df_template = pd.read_sql_query(
            "SELECT * FROM Function_Data WHERE FunctionId = ?", conn, params=[fun_id]
        )

        df_functions = pd.read_sql_query("SELECT * FROM Functions", conn)
        conn.commit()

        description = df_functions.loc[
            df_functions['FunctionName'] == selection_module, 'FunctionDescription'
        ].values[0] if selection_module in df_functions['FunctionName'].values else ""

        file_path = app_generate_CM_fb.functionBlock(
            f"All_CM_{selection_module}", description, selection_module, nr, df, df_template
        )

        logs.log_user_activity("The PLC Function Block File Exported")
        return file_path

    except Exception as e:
        return {"status": "error", "message": f"An error occurred while exporting rungs: {str(e)}"}

def _exportTiaDbSie(nr, selection_module, df, cmd_optimized_db):
    if not nr:
        return {"status": "error", "message": "Please enter PLC NR."}

    try:
        udt_dict = {
            'MTR': 'UDT_CM_MTR_N',
            'FRQ': 'UDT_CM_FRQ_N',
            'VLV': 'UDT_CM_VLV_N',
            'PID': 'UDT_CM_PID_N',
            'AIN': 'UDT_CM_AIN_N',
            'AOUT': 'UDT_CM_AOUT_N',
            'DIN': 'UDT_CM_DIN_N',
            'ALM': 'UDT_CM_ALM',
            'ILK': 'UDT_CM_ILK_N'
        }

        if selection_module not in udt_dict:
            return {"status": "error", "message": f"No UDT mapping found for module: {selection_module}"}

        file_path = app_generate_cm_db.dataBlock(
            dbNamePrefix="dbPlcHmi",
            cmName=selection_module,
            UDT=udt_dict[selection_module],
            optDb=cmd_optimized_db,
            df=df,
            nr=nr
        )

        logs.log_user_activity("The PLC DataBlock File Exported")
        return file_path

    except Exception as e:
        return {"status": "error", "message": f"An error occurred while exporting DB: {str(e)}"}

def _exportPlcTextlistSie(nr, selection_module, df):
    if not nr:
        return {"status": "error", "message": "Please enter PLC NR."}

    try:
        file_path = app_plc_textlists.GeneratePlcTextlists(df, nr, selection_module, 'CM_Item_')
        logs.log_user_activity("The PLC Textlist File Exported")
        return file_path

    except Exception as e:
        return {"status": "error", "message": f"An error occurred while exporting Textlist: {str(e)}"}

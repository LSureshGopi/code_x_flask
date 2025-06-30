
from model.siemens.scada_wincc_sqldb import app_wincc_sqldb
def _exportScadaWinccSqldb(nr, df, refPdfPath, selectionModule, electDocFilepath):
    if nr == "":
        return "Please enter PLC NR."
    try:
        if selectionModule == "MTR":
            column_dict = {'Description': 'Description'}
            objects = ['Id', 'ItemNumber', 'Description',
                        'PdfElectSchemaPath', 'PdfElectSchemaPage']
            app_wincc_sqldb.GenerateWinccSqldb(
                df, nr, selectionModule, electDocFilepath, refPdfPath, objects, column_dict)
            return "Siemens WinCC_"+selectionModule + " Sql db Exported Successfully"

        elif selectionModule == "FRQ":
            column_dict = {'Description': 'Description',
                            'IpAddress': 'IP Address'}
            column_defaultvalue_dict = {
                'PdfVfdSchemaPath': 'C:\\Users\\Public\\Documents\\Siemens\\WinCCProjects\\SinamicsG120-CU250S.pdf', 'PdfVfdSchemaPage': '1349'}
            objects = ['Id', 'ItemNumber', 'Description', 'IpAddress', 'PdfElectSchemaPath',
                        'PdfElectSchemaPage', 'PdfVfdSchemaPath', 'PdfVfdSchemaPage']  
            app_wincc_sqldb.GenerateWinccSqldb(
                df, nr, selectionModule, electDocFilepath, refPdfPath, objects, column_dict, column_defaultvalue_dict)
            return "Siemens WinCC_"+ selectionModule + " Sql db Exported Successfully"
                        
        elif selectionModule == "AIN":
            column_dict = {'Description': 'Description',
                            'Unit': 'EU', 'IoAddress': 'PLC Tag Name'}
            objects = ['Id', 'ItemNumber', 'Description', 'Process', 'Unit',
                        'IoAddress', 'PdfElectSchemaPath', 'PdfElectSchemaPage']
            app_wincc_sqldb.GenerateWinccSqldb(
                df, nr, selectionModule, electDocFilepath, refPdfPath, objects, column_dict)
            return "Siemens WinCC_"+selectionModule + " Sql db Exported Successfully"

        elif selectionModule == "AOUT":
            column_dict = {'Description': 'Descr iption',
                            'Unit': 'EU', 'IoAddress': 'PLC Tag Name'}
            objects = ['Id', 'ItemNumber', 'Description', 'Process', 'Unit',
                        'IoAddress', 'PdfElectSchemaPath', 'PdfElectSchemaPage']
            app_wincc_sqldb.GenerateWinccSqldb(
                df, nr, selectionModule, electDocFilepath, refPdfPath, objects, column_dict)
            return "Siemens WinCC_"+selectionModule + " Sql db Exported Successfully"

        elif selectionModule == "DIN":
            column_dict = {'Description': 'Description',
                            'IoAddress': 'PLC Tag Name'}
            objects = ['Id', 'ItemNumber', 'Description',
                        'IoAddress', 'PdfElectSchemaPath', 'PdfElectSchemaPage']
            app_wincc_sqldb.GenerateWinccSqldb(
                df, nr, selectionModule, electDocFilepath, refPdfPath, objects, column_dict)
            return "Siemens WinCC_"+selectionModule + " Sql db Exported Successfully"

        elif selectionModule == "VLV":
            column_dict = {
                'Description': 'Description', 'Type': 'Cfg Type'}
            objects = ['Id', 'ItemNumber', 'Description', 'IoAddress',
                        'PdfElectSchemaPath', 'PdfElectSchemaPage', 'Type']
            app_wincc_sqldb.GenerateWinccSqldb(
                df, nr, selectionModule, electDocFilepath, refPdfPath, objects, column_dict)
            return "Siemens WinCC_"+selectionModule + " Sql db Exported Successfully"  

        elif selectionModule == "PID":
            column_dict = {'Description': 'Description',
                            'Unit': 'EU', 'IoAddress': 'PLC Tag Address'}
            objects = ['Id', 'ItemNumber', 'Description', 'Process', 'Unit',
                        'IoAddress', 'PdfElectSchemaPath', 'PdfElectSchemaPage']
            app_wincc_sqldb.GenerateWinccSqldb(
                df, nr, selectionModule, electDocFilepath, refPdfPath, objects, column_dict)
            return "Siemens WinCC_"+selectionModule + " Sql db Exported Successfully"

    except Exception as e:
        return ("An error occured when trying to export Sql db " + str(e))

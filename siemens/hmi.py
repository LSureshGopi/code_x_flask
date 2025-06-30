# Siemens code generators
from model.siemens.tia_hmi_tags import app_hmi_tags
from model.siemens.scada_wincc_sqldb import app_wincc_sqldb
from model.siemens.tia_textlists import app_plc_textlists, app_hmi_textlists



def _exportTiaHmiTags(df, nr, selectionModule):  # Export HMI Tags - button #####
    if nr == "":
        return "Please enter PLC NR."
    try:
        UDTdict = {'MTR': 'UDT_CM_MTR_N', 'FRQ': 'UDT_CM_FRQ_N', 'VLV': 'UDT_CM_VLV_N', 'PID': 'UDT_CM_PID_N',
                    'AIN': "UDT_CM_AIN_N", 'AOUT': "UDT_CM_AOUT_N", 'DIN': "UDT_CM_DIN_N", 'ALM': "UDT_CM_ALM"}
        
        app_hmi_tags.GenerateHMITags(
            df, nr, selectionModule, UDTdict[selectionModule], 'HMI_Connection_1', 'dbPlcHmi')
        return "Siemens HMI_"+selectionModule + " HMI_TAG Exported Successfully"

    except Exception as e:
        return ("An error occured when trying to export HMI tags" + str(e))
    

# ----------------Export Siemens HMI Text Lists----------------
def _exportHmiTextlistSie(df, nr, selectionModule):
    if nr == "":
        return "Please enter PLC NR."
    try:
        app_hmi_textlists.GenerateHmiTextlists(
            df, nr, selectionModule, 'CM_Item_')
        return "Siemens HMI_" + selectionModule + " Textlist exported Successfully"

    except Exception as e:
        return ("An error occured when trying to export HMI textlists" + str(e))





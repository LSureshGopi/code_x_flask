import pandas as pd
import tempfile
import os
# Create Text lists for PLC
def GeneratePlcTextlists(df, nr, Name, NamePrefix):

    Plc_Textlists_list = list()
    for i in range(len(df)):
        # Dictionary for TIA HMI tag formats
        Plc_Textlists_dict = {'Parent': f'{NamePrefix}{Name}',
                              'From': str(df.loc[i]["CM No"]),
                              'To': str(df.loc[i]["CM No"]),
                              'Text [en-US]': df.loc[i]["Description"]
                              }
        Plc_Textlists_list.append(Plc_Textlists_dict)
        Plc_Textlists_df = pd.DataFrame(Plc_Textlists_list)

    TextList_dict = {'Name': {0: f'{NamePrefix}{Name}'},
                     'ListRange': {0: 'Decimal'},
                     'Comment [en-US]': {0: 'Item name for ControlModules'},
                     }

    df_TextList = pd.DataFrame(TextList_dict)
    temp_dir = tempfile.gettempdir()
    filename = os.path.join(temp_dir, f"{Name}_Plc_alarm_Textlists.xlsx")
    # with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df_TextList.to_excel(writer, sheet_name='TextList', index=False)
        Plc_Textlists_df.to_excel(writer, sheet_name='TextListEntry', index=False)
        # TIA Portal requires custom properties to be set in the .xlsx file
        writer.book.set_custom_property('FileVersion', '1')
        writer.book.set_custom_property('FileContent', 'Alarm text lists')

    return filename

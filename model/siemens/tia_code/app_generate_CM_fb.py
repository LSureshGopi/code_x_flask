from ast import IsNot
import pandas as pd
import tempfile
import os

def functionBlock(FBName, LibName, DbName, nr, df, dfTemplate):
    temp_dir = tempfile.gettempdir()
    filename = os.path.join(temp_dir, f"{FBName}.awl")

    with open(filename, 'w') as f:
        L1 = []
        L1.append(str(f'FUNCTION_BLOCK "{FBName}"\n'))
        L1.append(str("TITLE = Control module\n"))
        L1.append(str("{ S7_Optimized_Access := 'TRUE' }\n"))
        L1.append(str("VERSION : 0.1\n"))
        L1.append(str(" VAR\n"))
        L1.append(str(" END_VAR\n\n\n"))
        L1.append(str("BEGIN\n"))
        f.writelines(L1)

        for i in range(len(df)):
            CM_dict = {}
            Tag = str(df.loc[i]["Tag"])
            Description = str(df.loc[i]["Description"])

            for j in range(len(dfTemplate)):
                obj = dfTemplate.loc[j]["Objects"]
                if not pd.isnull(dfTemplate.loc[j]["WorksheetColumnName"]):
                    key = dfTemplate.loc[j]["WorksheetColumnName"]
                    if not pd.isnull(df.loc[i][key]):
                        CM_dict[obj] = df.loc[i][key]
                    elif not pd.isnull(dfTemplate.loc[j]["DefaultValues"]):
                        CM_dict[obj] = dfTemplate.loc[j]["DefaultValues"]
                    else:
                        CM_dict[obj] = ""
                elif not pd.isnull(dfTemplate.loc[j]["DefaultValues"]):
                    CM_dict[obj] = dfTemplate.loc[j]["DefaultValues"]
                else:
                    CM_dict[obj] = ""

            CM_No = CM_dict.get('CM_No')
            L2 = []
            L2.append("NETWORK\n")
            L2.append(f'TITLE = {CM_No} - {Tag} - {Description}\n\n')
            L2.append(f'       CALL #"{Tag}"\n')
            L2.append("       (\n")

            for k in range(len(dfTemplate)):
                obj = dfTemplate.loc[k]["Objects"]
                if obj == f"CM_{DbName}":
                    L2.append(f'         CM_{DbName}        := "dbPlcHmi{DbName}".{DbName}[{CM_No}] ,\n')
                elif CM_dict[obj] == "nan":
                    L2.append(f'         {obj}       := ,\n')
                elif CM_dict[obj] != "":
                    L2.append(f'         {obj}       := {CM_dict[obj]} ,\n')

            L2.append("       );\n\n")
            f.writelines(L2)

    for i in range(len(df)):
        with open(filename, 'r') as f:
            contents = f.readlines()
        Tag = str(df.loc[i]["Tag"])
        L3 = f'   "{Tag}" : "{LibName}";\n'
        Line = 5+i
        contents.insert(Line, L3)

        with open(filename, "w") as f:
            f.writelines(contents)

    with open(filename, 'a') as f:
        f.write("END_FUNCTION_BLOCK\n")

    return filename













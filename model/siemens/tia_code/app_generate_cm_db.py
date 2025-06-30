
import tempfile
import os

def dataBlock(dbNamePrefix, cmName, UDT, optDb, df, nr):
    temp_dir = tempfile.gettempdir()
    filename = os.path.join(temp_dir, f"{cmName}.db")

    with open(filename, 'w') as f:
        L0 = str(len(df))
        arrMinIndex = min(df["CM No"]) - 1
        arrMaxIndex = max(df["CM No"]) + 5

# TIA DB Format (Fixed Text)
        L1 = []
        L1.append(str(f'DATA_BLOCK "{dbNamePrefix}{cmName}"\n'))
        if optDb:
            L1.append(str("{ S7_Optimized_Access := 'TRUE' }\n"))
        else:
            L1.append(str("{ S7_Optimized_Access := 'FALSE' }\n"))
        L1.append(str("VERSION : 0.1\n"))

        L1.append(str(" STRUCT\n"))
        L1.append(
            str(f'   {cmName} : Array[{arrMinIndex}..{arrMaxIndex}] of "{UDT}";\n'))

        L1.append(str(" END_STRUCT;\n"))
        L1.append(str("\n"))
        L1.append(str("BEGIN\n"))
        L1.append(str("END_DATA_BLOCK\n"))

        f.writelines(L1)
        f.close()
    return filename
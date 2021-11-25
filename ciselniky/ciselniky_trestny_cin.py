import pandas

DATABASE_CONNECTION = "mssql+pymssql://sa:Mokra.114@localhost:1433/czechitas"
OUTPUT_TABLE_LEVEL_1 = "ciselnik_1_uroven"
OUTPUT_TABLE_LEVEL_2 = "ciselnik_2_uroven"
OUTPUT_TABLE_LEVEL_3 = "ciselnik_3_uroven"
OUTPUT_TABLE_LEVEL_4 = "ciselnik_4_uroven"

df_ciselnik_4_uroven = pandas.DataFrame()
df_ciselnik_4_uroven = pandas.read_excel(
        io = ".\\data\\ciselnik_4_uroven.xlsx",
        nrows = 303,
        usecols = "A:C"
        )
#print(df_ciselnik_4_uroven)

df_ciselnik_4_uroven.to_sql(OUTPUT_TABLE_LEVEL_4, DATABASE_CONNECTION, if_exists = "replace")

df_ciselnik_3_uroven = pandas.DataFrame()
df_ciselnik_3_uroven = pandas.read_excel(
        io = ".\\data\\ciselnik_3_uroven.xlsx",
        nrows = 12,
        usecols = "A:C"
        )
#print(df_ciselnik_3_uroven)

df_ciselnik_3_uroven.to_sql(OUTPUT_TABLE_LEVEL_3, DATABASE_CONNECTION, if_exists = "replace")

df_ciselnik_2_uroven = pandas.DataFrame()
df_ciselnik_2_uroven = pandas.read_excel(
        io = ".\\data\\ciselnik_2_uroven.xlsx",
        nrows = 9,
        usecols = "A:C"
        )
#print(df_ciselnik_2_uroven)

df_ciselnik_2_uroven.to_sql(OUTPUT_TABLE_LEVEL_2, DATABASE_CONNECTION, if_exists = "replace")

df_ciselnik_1_uroven = pandas.DataFrame()
df_ciselnik_1_uroven = pandas.read_excel(
        io = ".\\data\\ciselnik_1_uroven.xlsx",
        nrows = 6,
        usecols = "A:B"
        )
#print(df_ciselnik_1_uroven)

df_ciselnik_1_uroven.to_sql(OUTPUT_TABLE_LEVEL_1, DATABASE_CONNECTION, if_exists = "replace")
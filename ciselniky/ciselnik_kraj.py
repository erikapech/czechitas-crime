import pandas

DATABASE_CONNECTION = "mssql+pymssql://sa:Mokra.114@localhost:1433/czechitas"
OUTPUT_TABLE = "kraj"

df_kraj_ciselnik = pandas.DataFrame()
df_kraj_ciselnik = pandas.read_excel(
        io = ".\\data\\kraj_ciselnik.xlsx",
        nrows = 15,
        usecols = "A:B"
        )
print(df_kraj_ciselnik)

df_kraj_ciselnik.to_sql(OUTPUT_TABLE, DATABASE_CONNECTION, if_exists = "replace")
import pandas
from sqlalchemy.types import Integer
#vytvoreni dataframu a nacteni hodnot, preskocena hlavicka

DATABASE_CONNECTION = "mssql+pymssql://sa:Mokra.114@localhost:1433/czechitas"
OUTPUT_TABLE = "obyvatelstvo"
PATH_RAW_DATA = ".\\data\\"
POCATECNI_ROK = 2016
KONECNY_ROK = 2020 + 1      #nacte rok 2020 
POCATECNI_MESIC = 1
KONECNY_MESIC = 12 + 1      #nacte 12 mesicu

def zpracovani_obyvatelstvo(jmeno_souboru):
    df_obyvatelstvo = pandas.DataFrame()
    month_obyvatelstvo = pandas.read_excel(
            io = jmeno_souboru,
            header = None,
            skiprows = 6,
            nrows = 101,
            usecols = "A, K:X"
            )
    df_obyvatelstvo = df_obyvatelstvo.append(month_obyvatelstvo)
    return df_obyvatelstvo

#soubor s obyvatelstvem mam jen jedny data za rok, tak ho duplikuji pro kazdy mesic
df_obyvatelstvo = pandas.DataFrame()
for rok in range(POCATECNI_ROK, KONECNY_ROK):
    for mesic in range(POCATECNI_MESIC, KONECNY_MESIC):
        jmeno_souboru = f"{PATH_RAW_DATA}obyvatelstvo_{rok}_01.xlsx"
        datum = f"{rok}-{mesic}"
        df_obyvatelstvo_tento_mesic = zpracovani_obyvatelstvo(jmeno_souboru)
        #pridani pojmenovani sloupců
        df_obyvatelstvo_tento_mesic.columns = ["vek", 
                                    "CZ010",
                                    "CZ020",
                                    "CZ031",
                                    "CZ032",
                                    "CZ041",
                                    "CZ042",
                                    "CZ051",
                                    "CZ052",
                                    "CZ053",
                                    "CZ063",
                                    "CZ064",
                                    "CZ071",
                                    "CZ072",
                                    "CZ080"]
        #transformace wide table na long table
        df_obyvatelstvo_tento_mesic = pandas.melt(df_obyvatelstvo_tento_mesic, id_vars=["vek"], var_name = "kraj", value_name = "pocet_obyvatel")
        df_obyvatelstvo_tento_mesic["datum"]= pandas.Period(datum, freq="M").end_time.date()
        df_obyvatelstvo = df_obyvatelstvo.append(df_obyvatelstvo_tento_mesic)
        #nahradím věkovou kategorii 100+ jen číslem 100, spodní hranice
        df_obyvatelstvo = df_obyvatelstvo.replace(to_replace = "100+", value = "100")
        #print(df_obyvatelstvo)
print("Exportuji do databáze")
#df_obyvatelstvo.to_sql(OUTPUT_TABLE, DATABASE_CONNECTION, if_exists = "replace", dtype = {"vek": Integer()})

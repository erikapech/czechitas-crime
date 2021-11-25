import pandas
import json

DATABASE_CONNECTION = "mssql+pymssql://sa:Mokra.114@localhost:1433/czechitas"
OUTPUT_TABLE = "nezamestnanost"
CESTA_HRUBA_DATA = ".\\data\\"
POCATECNI_ROK = 2016
KONECNY_ROK = 2020 + 1      #nacte rok 2020 
POCATECNI_MESIC = 1
KONECNY_MESIC = 12 + 1      #nacte 12 mesicu

#datum ve formátu yyyy-mm nahradim datum posledniho dne v mesici
#pridani sloupce kraj pres ciselnik okresy a kraje ze stranek mpsv
#odstranění dupicitního sloupce s kodem okresu
def zpracovani_json_souboru(nazev_souboru, datum_souboru):
    with open (nazev_souboru) as nezamestnanost_data:
        data = json.load(nezamestnanost_data)   #vysledkem je slovnik
    seznam_hodnot = data["polozky"]
    df_nezamestanost_data = pandas.DataFrame(seznam_hodnot)
    df_nezamestanost_data["datum"] = pandas.Period(datum, freq="M").end_time.date()
    df_nezamestanost_data_kraj = pandas.merge(df_nezamestanost_data, df_okres_kraj_ciselnik, left_on="okres", right_on= "id_x")
    df_nezamestanost_data_kraj = df_nezamestanost_data_kraj.drop(["id_x"], axis = 1)
    return df_nezamestanost_data_kraj

#vytvoreni ciselniku s kody okresu a kraju podle CSU NUTS3
#importovani dat ciselnik okresy, vytvoreni dataframu s daty za okresy
with open (f"{CESTA_HRUBA_DATA}okresy.json", encoding="utf-8") as okresy:
    data_okresy = json.load(okresy)

seznam_hodnot_okresy = data_okresy["polozky"]
df_okresy = pandas.DataFrame(seznam_hodnot_okresy)
print(df_okresy["kraj"])

#importovani dat ciselnik kraje, vytvoreni dataframu s daty za kraje
with open (f"{CESTA_HRUBA_DATA}kraje.json", encoding="utf-8") as kraje:
    data_kraje = json.load(kraje)

seznam_hodnot_kraje = data_kraje["polozky"]
df_kraje = pandas.DataFrame(seznam_hodnot_kraje)
print(df_kraje)

#inner join df_okresy, df_kraje, k okresu je přidán daný kraj
df_okres_kraj = pandas.merge(df_okresy, df_kraje, left_on= "kraj", right_on= "id")
print(df_okres_kraj.columns)

#vybrala jsem jen sloupec, kde jse číslo okresu a sloupec s číslem kraje
df_okres_kraj_ciselnik = df_okres_kraj[["id_x", "kodNuts3"]]
print(df_okres_kraj_ciselnik)

df_nezamestnanost = pandas.DataFrame()
#vytvorim si jmena souboru s daty
for rok in range(POCATECNI_ROK, KONECNY_ROK):
    for mesic in range(POCATECNI_MESIC, KONECNY_MESIC):
        jmeno_souboru = f"{CESTA_HRUBA_DATA}nezamestnanost_{rok}_{mesic:02}.json"
        datum = f"{rok}-{mesic}"
        df_nezamestnanost = df_nezamestnanost.append(zpracovani_json_souboru(jmeno_souboru, datum))
print(df_nezamestnanost)

print("Exportuji do databáze")
#df_nezamestnanost.to_sql(OUTPUT_TABLE, DATABASE_CONNECTION, if_exists = "replace")
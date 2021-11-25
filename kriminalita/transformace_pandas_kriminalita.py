from numpy import NaN
import pandas
from pandas.core.frame import DataFrame

DATABASE_CONNECTION = "mssql+pymssql://sa:Mokra.114@localhost:1433/czechitas"
OUTPUT_TABLE = "kriminalita"
CESTA_HRUBA_DATA = ".\\data\\"
POCATECNI_ROK = 2016
KONECNY_ROK = 2020 + 1      #nacte rok 2020 
POCATECNI_MESIC = 1
KONECNY_MESIC = 12 + 1      #nacte 12 mesicu

#slovník mi smlouží při převodu jmena kraje na kod NUTS
kraj = {"Praha" : "CZ010",
        "Středočeský" : "CZ020",
        "Jihočeský" : "CZ031",
        "Plzeňský" : "CZ032",
        "Karlovarský" : "CZ041",
        "Ústecký" : "CZ042",
        "Liberecký" : "CZ051",
        "Královéhradecký" : "CZ052",
        "Pardubický" : "CZ053",
        "Vysočina" : "CZ063",
        "Jihomoravský" : "CZ064",
        "Olomoucký" : "CZ071",
        "Zlínský" : "CZ072",
        "Moravskoslezský" : "CZ080" }


# month je slovnik, kde klic je nazev kraje a hodnota jsou trestné činy pro daný kraj(dataframe)
#touto funkcí načtu každý excelový soubor, názvy načítaných listů je seznam klíčů ze slovníku kraj
#potřebujeme přeskočit hlavičku a i nazvy sloupců, jsou to sloučené buňky
#stanovíme si kolik řádku a které sloupce potřebujeme z excelu
def zpracovani_souboru(nazev_souboru, datum_souboru):
    df_trestne_ciny = pandas.DataFrame()
    month_dict = pandas.read_excel(
        io = nazev_souboru,
        sheet_name = list(kraj.keys()),
        header = None,
        skiprows = 6,
        nrows = 400,
        usecols = "A, C:D, F:W"
        )
#z každého listu udělám df_kraj a přidám tam hlavičku, sloupec se jménem kraje
# df_kraj připojím do celého dataframu, kde budou všechny kraje
    for jmeno_kraje in month_dict:
        df_kraj = month_dict[jmeno_kraje]
        df_kraj.columns = ["id_cin",
                            "registrovano_pocet",
                            "objasneno_pocet",
                            "objasneno_spachano_nezletilymi",
                            "objasneno_spachano_mladistvymi",
                            "objasneno_spachano_detmi",
                            "objasneno_spachano_recidivisty",
                            "objasneno_spachano_cizinci",
                            "objasneno_spachano_pod_vlivem",
                            "objasneno_spachano_alkohol",
                            "objasneno_dodatecne_z_lonska",
                            "objasneno_celkem_pocet",
                            "objasneno_celkem_spachano_nezletilymi",
                            "objasneno_celkem_spachano_mladistvymi",
                            "objasneno_celkem_spachano_detmi",
                            "objasneno_celkem_spachano_recidivisty",
                            "objasneno_celkem_spachano_cizinci",
                            "objasneno_celkem_spachano_pod_vlivem",
                            "objasneno_celkem_spachano_alkohol",
                            "skoda_celkem_tisice",
                            "zajistene_hodnoty_tisice"
                            ]
        # kolik radku ma nacist, hledam prvni prazdny radek
        for cislo_radek, radek in df_kraj.iterrows():
            if pandas.isna(radek["id_cin"]):
                konec_dataframu = cislo_radek
                break
        #df_kraj = df_kraj.iloc[0:konec_dataframu]
        df_kraj = df_kraj.head(konec_dataframu)
        df_kraj["kraj"] = kraj[jmeno_kraje]
        df_trestne_ciny = df_trestne_ciny.append(df_kraj)
    #nastavení indexu na soubor, které se bude skládat z 1.sloupce excelu a kodu kraje
    #použiji to při odčítání dataframu
    return df_trestne_ciny.set_index(["id_cin", "kraj"])    
    
#vytvořím si dataframe, kam se postupně nahrají všechny dataframy s hodnotami za každý dílčí měsíc
df_vsechny_trestne_ciny = pandas.DataFrame()
#vytvorim si promennou pro odcitani dataframu a nastavim si to hodnotu None
df_predchozi_mesic = None

#díky cyklu si vytvořím proměnnou rok a měsíc, které použiji při načítání souboru a pro vytvoření datumu
for rok in range(POCATECNI_ROK, KONECNY_ROK):
    for mesic in range(POCATECNI_MESIC, KONECNY_MESIC):
        jmeno_souboru = f"{CESTA_HRUBA_DATA}trestne_ciny_{rok}_{mesic:02}.xlsx"
        datum = f"{rok}-{mesic}"
        #vysledek_funkce = zpracovani_souboru(jmeno_souboru, datum)
        df_trestne_ciny_tento_mesic = zpracovani_souboru(jmeno_souboru, datum)
#prvni soubor v každém roce není potřeba odčítat, měsíční přírůstek jsou data tohoto měsíce 
# přidán sloupec datum
# měsíční přírůstek je připojen do výsledného df_vsechny_trestne_ciny   
        if mesic == 1:
            df_predchozi_mesic = df_trestne_ciny_tento_mesic
            df_mesicni_prirustek = df_trestne_ciny_tento_mesic.copy()
            df_mesicni_prirustek["datum"] = (pandas.Period(datum, freq="M").end_time.date())
            df_vsechny_trestne_ciny = df_vsechny_trestne_ciny.append(df_mesicni_prirustek)
#ostatní měsíce odečítám dataframe následující od dataframu předchozího
#když skončil nebo přibyl kód trestného činu, tak to počítá NaN hodnoty
#když kód skončil, tak řádek v následujícím dataframu mažu
#když kód přibyl, tak chci v tomto řádku mít hodnoty tohoto měsíce
        else:
            df_mesicni_prirustek = df_trestne_ciny_tento_mesic.subtract(df_predchozi_mesic)
            #prochazim dataframe a hledam radky, kde je registovano_pocet NaN, klic je id_cin a kraj
            for klic, radek in df_mesicni_prirustek.iterrows():
                #pokud má řádek ve sloupci registovano hodnut Nan
                if pandas.isna(radek["registrovano_pocet"]): 
                    #pokud kod trestneho cinu byl naposledy v predachzejicim mesici, radek v mesicnim prirustku smazeme
                    if klic in df_predchozi_mesic.index:
                        df_mesicni_prirustek = df_mesicni_prirustek.drop(index = klic)
                    else:
                        df_mesicni_prirustek.loc[klic] = df_trestne_ciny_tento_mesic.loc[klic]   
            df_mesicni_prirustek["datum"] = (pandas.Period(datum, freq="M").end_time.date())
            df_vsechny_trestne_ciny = df_vsechny_trestne_ciny.append(df_mesicni_prirustek)
            #při prvním běhu cyklu se mi proměnná před cyklem s hodnotou None 
            df_predchozi_mesic = df_trestne_ciny_tento_mesic
        print(f"Zpracovávám soubor:{jmeno_souboru}")  
#export do databaze
print("Exportuji do databáze")
#df_vsechny_trestne_ciny.reset_index().to_sql(OUTPUT_TABLE, DATABASE_CONNECTION, if_exists = "replace")
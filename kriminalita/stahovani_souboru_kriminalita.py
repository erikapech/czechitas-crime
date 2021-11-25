from urllib import request
import time

CESTA_POLICIE_ZACATEK = "https://www.policie.cz/soubor/"
CESTA_POLICIE_KONEC = "-sest-01a-xlsx.aspx"
CESTA_HRUBA_DATA = ".\\data\\"
POCATECNI_ROK = 2016
KONECNY_ROK = 2020 + 1      #nacte rok 2020 
POCATECNI_MESIC = 1
KONECNY_MESIC = 12 + 1      #nacte 12 mesicu


mesic_nazev = {1 : "leden",
               2 : "unor",
               3 : "brezen",
               4 : "duben",
               5 : "kveten",
               6 : "cerven",
               7 : "cervenec",
               8 : "srpen",
               9 : "zari",
               10 : "rijen",
               11 : "listopad",
               12 : "prosinec"}

def stahovani_souboru(url, ulozeny_soubor):
    request.urlretrieve(url, ulozeny_soubor)

for rok in range(POCATECNI_ROK, KONECNY_ROK):
    for mesic in range (POCATECNI_MESIC, KONECNY_MESIC):
        mesic_jmeno = mesic_nazev[mesic]
        url_souboru = f"{CESTA_POLICIE_ZACATEK}{rok}-{mesic:02}-{mesic_jmeno}{CESTA_POLICIE_KONEC}"
        jmeno_souboru = f"{CESTA_HRUBA_DATA}trestne_ciny_{rok}_{mesic:02}.xlsx"
        stahovani_souboru(url_souboru, jmeno_souboru)
        print(mesic_jmeno)
        print(url_souboru)
        print(jmeno_souboru)
        time.sleep(3) #prevence zvyseneho provozu na serveru



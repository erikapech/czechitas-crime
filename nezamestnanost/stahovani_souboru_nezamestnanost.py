from urllib import request
import time


CESTA_MPSV_ZACATEK = "https://data.mpsv.cz/od/soubory/nezamestnanost-mesicni/nezamestnanost-mesicni-"
CESTA_MPSV_KONEC = ".json"
CESTA_HRUBA_DATA = "\\data\\"
POCATECNI_ROK = 2016
KONECNY_ROK = 2020 + 1      #nacte rok 2020 
POCATECNI_MESIC = 1
KONECNY_MESIC = 12 + 1      #nacte 12 mesicu

def stahovani_souboru(url, ulozeny_soubor):
    request.urlretrieve(url, ulozeny_soubor)

for rok in range(POCATECNI_ROK, KONECNY_ROK):
    for mesic in range (POCATECNI_MESIC, KONECNY_MESIC):
        url_souboru = f"{CESTA_MPSV_ZACATEK}{mesic:02}-{rok}{CESTA_MPSV_KONEC}"
        jmeno_souboru = f"{CESTA_HRUBA_DATA}nezamestnanost_{rok}_{mesic:02}.json"
        stahovani_souboru(url_souboru, jmeno_souboru)
        print(url_souboru)
        print(jmeno_souboru)
        time.sleep(3) #prevence zvyseneho provozu na serveru



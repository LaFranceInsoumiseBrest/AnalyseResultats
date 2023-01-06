import os
import json
import time
import random
import pandas as pd
from collections import defaultdict
from selenium import webdriver 
from selenium.webdriver.common.by import By

#bureaux = json.load("bureaux.json")

# example_url = "https://www.brest.fr/fileadmin/imported_for_brest/fileadmin/resultats_electoraux/2022-legislatives/premier-tour/HTML/index.html#/RESULT_049_001_001_027"

# f = open('urls_bureaux_1ertour_test.json')
# urls_list = json.load(f)
# f.close()

url_tour = {}
url_tour[1] = "https://www.brest.fr/fileadmin/imported_for_brest/fileadmin/resultats_electoraux/2022-legislatives/premier-tour/HTML/index.html"
url_tour[2] = "https://www.brest.fr/fileadmin/imported_for_brest/fileadmin/resultats_electoraux/2022-legislatives/second-tour/HTML/index.html"
output_dir = "resultats"


# PARAMETRES ENTREE
# circo : 2 ou 3
circo = 2
# tour : 1 ou 2
tour = 2
# True ou False
test = False

#result_dict = defaultdict(list)
result_list = []

driver = webdriver.Firefox()
driver.implicitly_wait(3)

driver.get(url_tour[tour])

if circo == 2:
    links = driver.find_elements(By.XPATH, "//td[@class='liste']/a")
    if len(links) == 0 :
        raise("Bug de la page : relancez svp")

    links_dict = {link.text: {"url": link.get_attribute("href"), 
                              "circo": circo, "tour": tour}  
                  for link in links}

driver.quit()
# POUR TEST
if test :
    links_dict = dict(random.sample(links_dict.items(), 3))
    output_dir = "test"


for bureau, prop in links_dict.items():
    url = prop["url"]
    circo = prop["circo"]
    tour = prop["tour"]

    result_dict = dict()
    success = False 
    retry = 0
    while not success and retry < 3 :
        print(bureau + " : " + str(retry) )

        driver = webdriver.Firefox()
        driver.implicitly_wait(3)

        driver.get(url)
        result_dict["Bureau"] = bureau
        result_dict["Circo"] = circo
        result_dict["Tour"] = tour

        # Récupérer le bureau de vote
        #bureau = driver.find_element(By.XPATH, "//p[@class='res bold info-text color-background']").text.split(' : ')[1]
        #result_dict["Bureau de vote"].append(bureau)

        # Récupérer les méta-données du vote
        meta = driver.find_elements(By.XPATH, "//*[@class='mdl-cell mdl-cell--3-col mdl-cell--2-col-phone']")
        meta_dict = {}
        if len(meta) == 0:
            retry = retry + 1
        else:
            for elem in meta : 
                titre, valeur = elem.text.split(' : ')
                result_dict[titre] = valeur

            gettext = lambda x: x.text

            # Récupérer les candidats 
            candidates = driver.find_elements(By.XPATH, "//span[@class='candidat']")

            # Récupérer les votes
            raw_votes = driver.find_elements(By.XPATH, "//span[@class='candidat padding-vote']")
            txt_votes = map(gettext, raw_votes)
            int_votes = map(lambda x : x.strip(" votes"), txt_votes)

            zipvotes = zip(map(gettext, candidates), int_votes)

            for (candidate, vote) in zipvotes :
                result_dict[candidate] = vote

            success = True
            
        driver.quit()
    result_list.append(result_dict)

print(result_list)

df = pd.DataFrame.from_records(result_list)
print(df)

os.makedirs(output_dir, exist_ok=True)
filename = "circo{}_tour{}.csv".format(circo, tour)
df.to_csv(output_dir + "/" + filename, sep=";")
# df
# Bureaux de vote | tour | inscrits | Total votants | Participation | Blancs | Nuls | Exprimés | Cadalen | Larso ...



#elements = driver.find_elements(By.XPATH, "//span[@class='candidat']")
# for elem in elements :
#     print(elem.text)

# resultat = driver.find_elements(By.XPATH, "//*[@id='resultat']//*[@class='mdl-grid']")

# for elem in resultat:
#     print(elem.text)


# Au final on ne peut pas réutiliser l'élément parent pour sélectionner les enfants
# resultat = driver.find_element(By.ID, "resultat")
# print(driver.find_element(By.XPATH, "//p[@class='res bold info-text color-background']"))

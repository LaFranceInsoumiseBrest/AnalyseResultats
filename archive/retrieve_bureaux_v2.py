import json
import pandas as pd
from selenium import webdriver 
from selenium.webdriver.common.by import By

url_tour = {}
url_tour[1] = "https://www.brest.fr/fileadmin/imported_for_brest/fileadmin/resultats_electoraux/2022-legislatives/premier-tour/HTML/index.html"
url_tour[2] = "https://www.brest.fr/fileadmin/imported_for_brest/fileadmin/resultats_electoraux/2022-legislatives/second-tour/HTML/index.html"

# PARAMETRES ENTREE
# circo : 2 ou 3
circo = 2
# tour : 1 ou 2
tour = 1

driver = webdriver.Firefox()
driver.implicitly_wait(3)

driver.get(url_tour[tour])


if circo == 2:
    links = driver.find_elements(By.XPATH, "//td[@class='liste']/a")

    links_dict = {link.text: {"url": link.get_attribute("href"), 
                              "circo": circo, "tour": tour}  
                  for link in links}
    
    filename = "urls_bureaux_circo{}_tour{}.json".format(circo, tour)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(links_dict, f, ensure_ascii=False, indent=4)

driver.quit()






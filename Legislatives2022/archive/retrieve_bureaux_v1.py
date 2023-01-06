#!/Users/leolelonquer/opt/anaconda3/bin/python3

import xml.etree.ElementTree as ET 
import json
# La table contenant la liste des bureaux de s'appelle 
# <table id="bureau" class="liste-bureau">
#    <tbody>
#        <tr class="first-line"></tr><tr>
#         <td class="liste"><a id="RESULT_049_001_001_027" href="#/RESULT_049_001_001_027" onclick="afficherResultat(this)">027-MAIRIE CENTRALE</a></td></tr>
#        <tr><td class="liste"><a id="RESULT_049_001_001_028" href="#/RESULT_049_001_001_028" onclick="afficherResultat(this)">028-MAIRIE CENTRALE</a></td></tr>
#    </tbody>
# </table>

# Soluvote.xml est une sauvegarde Firefox dans laquelle je n'ai gardé que le body
parser = ET.parse('Soluvote.xml')

res = parser.findall(".//td[@class='liste']/a")

links_dict = {}
for link in res:
    links_dict[link.text] = base_url + link.get("href")

with open('bureaux.json', 'w', encoding='utf-8') as f:
    json.dump(links_dict, f, ensure_ascii=False, indent=4)


#print(links_dict)


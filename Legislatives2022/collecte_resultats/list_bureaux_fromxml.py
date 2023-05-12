import os
import sys
import xml.etree.ElementTree as ET 

def to_dict(bureaux_list):
    dico = {}
    for bureau in bureaux_list :
        for elem in bureau :
            if elem.tag == "numero" :
                numero = elem.text
            if elem.tag == "nom" :
                nom = elem.text
            elif elem.tag == "fichier" :
                fichier = elem.text
        full_name = numero + ";" + nom
        dico[full_name] = fichier
    return dico


def write_simple(dico, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as f:
        for full_name, fichier in dico.items():
            f.write("{};{}\n".format(full_name,fichier))
        

if __name__ == "__main__":
    try:
        input_file = sys.argv[1]
        output_dir = sys.argv[2]
    except :
        raise("Indique en paramètres le fichier d'entrée et le dossier de sortie")

    tree = ET.parse(input_file)
    root = tree.getroot()

    bureaux = root.findall(".//bureaux")
    bureaux_circo2 = bureaux[0]
    bureaux_circo3 = bureaux[1]
        
    circo2 = to_dict(bureaux_circo2)
    circo3 = to_dict(bureaux_circo3)

    output_circo2 = os.path.join(output_dir, "circo2.csv")
    output_circo3 = os.path.join(output_dir, "circo3.csv")

    write_simple(circo2, output_circo2)
    write_simple(circo3, output_circo3)

    print(output_circo2, output_circo3)
# with open("tmp/bureaux_circo2.json", 'w', encoding='utf-8') as f:
#     f.write(str(circo2))
#     #json.dump(circo2, f, ensure_ascii=False, indent=4)

# with open("tmp/bureaux_circo3.json", 'w', encoding='utf-8') as f:
#     json.dump(circo3, f, ensure_ascii=False, indent=4)




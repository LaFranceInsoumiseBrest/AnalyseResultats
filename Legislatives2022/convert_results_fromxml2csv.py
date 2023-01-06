import os 
import sys
import pandas as pd
import xml.etree.ElementTree as ET 

def get_data(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    result_dict = {}
    result_dict["Numéro"] = root.find(".//information/numero").text
    result_dict["Bureau"] = root.find(".//information/titre").text
    result_dict["Canton"] = root.find(".//information/canton").text
    result_dict["Circo"] = root.find(".//circonscription").text
    result_dict["Scrutin"] = root.find(".//scrutin").text
    result_dict["Inscrits"] = root.find(".//inscrits").text
    result_dict["Votants"] = root.find(".//votants").text
    result_dict["Blancs"] = root.find(".//blancs").text
    result_dict["Nuls"] = root.find(".//nuls").text
    result_dict["Exprimés"] = root.find(".//exprimes").text
    result_dict["Participation"] = root.find(".//participation").text

    candidats = root.findall(".//candidat")

    for candidat in candidats:
        data = {elem.tag : elem.text for elem in candidat}
        result_dict[data["intituler"] + " - votes"] = data["votes"]
        result_dict[data["intituler"] + " - pourcentage"] = data["pourcentage"]
    return result_dict


if __name__ == "__main__":
    try: 
        input_dir = sys.argv[1]
        result_file = sys.argv[2]
    except:
        input_dir = "tmp/circo2"

    result_list = []
    for filename in os.listdir(input_dir) :
        result_list.append(get_data(os.path.join(input_dir, filename)))

    df = pd.DataFrame.from_records(result_list)
    print(df)
    df.to_csv(result_file, sep=";")
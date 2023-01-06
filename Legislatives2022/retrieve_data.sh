#!/bin/bash

python="/Users/leolelonquer/opt/anaconda3/bin/python"

# Pour les tests utiliser avec seulement generate_csv avec ces deux paramètres
tour=1
circo=2

base_url_1ertour="https://www.brest.fr/fileadmin/imported_for_brest/fileadmin/resultats_electoraux/2022-legislatives/premier-tour/HTML/xml/"
base_url_2emetour="https://www.brest.fr/fileadmin/imported_for_brest/fileadmin/resultats_electoraux/2022-legislatives/second-tour/HTML/xml/"

generate_list_bureaux () {
    curl "${base_url}Election.xml" > $tmp_dir/Election.xml
    $python list_bureaux_fromxml.py $tmp_dir/Election.xml $tmp_dir
}

retrieve_votes () {
    in_file="$1"
    out_dir="$2"
    mkdir -p $out_dir
    cat $in_file | while read line; do
        numero=$(echo $line | cut -d';' -f1  )
        name=$(echo $line | cut -d';' -f2 )
        fichier=$(echo $line | cut -d';' -f3 )

        fichier_url="${base_url}${fichier}.xml"

        curl $fichier_url > "${out_dir}/${numero}"
    done
}


generate_csv () {
    if [[ $tour == 1 ]]; then
        base_url=$base_url_1ertour
    elif [[ $tour == 2 ]]; then
        base_url=$base_url_2emetour
    fi

    tmp_dir=tmp/tour$tour
    results_dir=resultats/

    mkdir -p $tmp_dir $results_dir

    generate_list_bureaux 

    # bureaux_files="tmp/tour1/circo2.csv"
    retrieve_votes "$tmp_dir/circo${circo}.csv" "$tmp_dir/circo$circo"

    #out_dirs="tmp/tour1/circo2"
    $python convert_results_fromxml2csv.py $out_dir "$results_dir/tour${tour}_circo${circo}.csv"
}

# generate_csv

for tour in 1 2; do 
    for circo in 2 3; do
        generate_csv
    done
done



    
    

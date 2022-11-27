#!/bin/bash

python="/Users/leolelonquer/opt/anaconda3/bin/python"

base_urls="https://www.brest.fr/fileadmin/imported_for_brest/fileadmin/resultats_electoraux/2022-legislatives/premier-tour/HTML/xml/ \
https://www.brest.fr/fileadmin/imported_for_brest/fileadmin/resultats_electoraux/2022-legislatives/second-tour/HTML/xml/"


retrieve_votes () {
    mkdir -p $out_dir
    cat $in_file | while read line; do
        numero=$(echo $line | cut -d';' -f1  )
        name=$(echo $line | cut -d';' -f2 )
        fichier=$(echo $line | cut -d';' -f3 )

        fichier_url="${base_url}${fichier}.xml"

        curl $fichier_url > "${out_dir}/${numero}"
    done
}


tour=1
for base_url in $base_urls ; do
    tmp_dir=tmp/tour$tour
    results_dir=resultats

    mkdir -p $tmp_dir $results_dir

    curl "${base_url}Election.xml" > $tmp_dir/Election.xml
    bureaux_files=$($python list_bureaux_fromxml.py $tmp_dir/Election.xml $tmp_dir)

    # bureaux_files="tmp/tour1/circo2.csv tmp/tour1/circo3.csv tmp/tour2/circo2.csv tmp/tour2/circo3.csv"
    out_dirs=""
    for bureau_file in $bureaux_files; do
        in_file="$bureau_file"
        circo=$(basename $bureau_file | cut -d. -f1)
        out_dir="$tmp_dir/$circo"
        retrieve_votes

        out_dirs="$out_dirs $out_dir"
    done

    #out_dirs="tmp/tour1/circo2 tmp/tour1/circo3 tmp/tour2/circo2 tmp/tour2/circo3"
    for out_dir in $out_dirs; do
        circo=$(basename $out_dir | cut -d. -f1)
        $python convert_results_fromxml2csv.py $out_dir "$results_dir/tour${tour}_${circo}.csv"
    done

    tour=$(($tour + 1))
done



    
    

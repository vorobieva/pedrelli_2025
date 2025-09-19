 #!/bin/bash
path_to_Tango='' # path to tango_x86_64_release
path_to_RaptorX='' # path to RaptorX oneline_command.sh

var=$(nproc) 
ls *.fasta | xargs -P $var -n 1 -I FILE "$path_to_RaptorX" FILE 1 0
cp */*.ss3_simp .
tar Jcf tmpRaptor.tar.xz */
for file in *.fasta
do 
    echo ${file:: -6} >> to_rm.list
done
if [ ! -d Raptor_Full_Output ]
then
	mkdir -p Raptor_Full_Output
fi
cat to_rm.list | xargs -P $var -n 1 -I FILE rm -r FILE/
mv tmpRaptor.tar.xz Raptor_Full_Output/
rm to_rm.list


n=1
m=1
mkdir T
echo -e "Sequence\tAggregation\tConc_Stab_Aggregation" >> tango_aggregation.txt
for file in *.fasta
do 
    echo "$n N N 7.0 298 0.02 $(echo $seq | awk -F: 'NR==2 {print $1}' ${file})" >> T/tango.list; 
    echo "${file%.fasta} $n" >> T/tango_index.txt; 
    echo "${file%.fasta} $m" >> tango_index.txt;
    "${path_to_Tango}" -inputfile=T/tango.list; 
    
    if [ $m -eq 1 ]
    then 
        mv 1.txt _1.txt
    fi
    
    if [ $m -gt 1 ]
    then 
        mv 1.txt $m.txt; 
    fi
    mv -n T/tango_aggregation.* T/tango_aggregation.txt 
    t=$(sed -n '2p' T/tango_aggregation.txt)
    tm=$(echo "$t" | cut -d ' ' -f 2-)
    echo -e "$m\t$tm" >> tango_aggregation.txt
    m=$((m+1))
    rm T/*
done
mv _1.txt 1.


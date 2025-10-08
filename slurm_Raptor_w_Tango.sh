#!/bin/bash
path_to_Tango='' # path to tango_x86_64_release
path_to_RaptorX='' # path to RaptorX oneline_command.sh

n=$(ls *.fasta | wc -l)
for file in *.fasta; do echo ${file:: -6} >> to_rm.list; done
N=$(ls *.fasta | wc -l)
m=$((($N+99) / 100))
k=0
i=0
for file in *.fasta
do
    if [[ $k == $m ]]
    then 
        k=0
        (( i++ ))
    fi
    (( k++ ))
    echo ${file} >> taskRaptor_${i}.list
done

ls taskRaptor_*.list >> main_Rapt.list

nj=$(cat main_Rapt.list | wc -l)

echo "#!/usr/bin/env bash" >> rapt.sbatch
echo "#SBATCH --time=30:00" >> rapt.sbatch
echo "#SBATCH --ntasks=1" >> rapt.sbatch
echo "#SBATCH --nodes=1" >> rapt.sbatch
echo "#SBATCH --cpus-per-task=1" >> rapt.sbatch
echo "#SBATCH --array=[1-"$nj"]""%100" >> rapt.sbatch
echo "input_file="'$'"(sed -n "'"''$'"SLURM_ARRAY_TASK_ID"'"'"p main_Rapt.list)" >> rapt.sbatch

echo "while read -r LINE" >> rapt.sbatch
echo "do" >> rapt.sbatch
echo "${path_to_RaptorX} "'$'"LINE 1 0" >> rapt.sbatch
echo "done < "'"''$'"input_file"'"' >> rapt.sbatch

echo "#!/usr/bin/env bash" >> postp.sbatch
echo "#SBATCH --time=1:00:00" >> postp.sbatch
echo "#SBATCH --ntasks=1" >> postp.sbatch
echo "#SBATCH --nodes=1" >> postp.sbatch
echo "#SBATCH --cpus-per-task=1" >> postp.sbatch
echo "cp */*.ss3_simp .">> postp.sbatch
echo "tar Jcf tmpRaptor.tar.xz */">> postp.sbatch
echo "if [ ! -d Raptor_Full_Output ]">> postp.sbatch
echo "then">> postp.sbatch
echo "	    mkdir -p Raptor_Full_Output">> postp.sbatch
echo "fi">> postp.sbatch
echo "cat to_rm.list | xargs -I FILE rm -r FILE/">> postp.sbatch
echo "mv tmpRaptor.tar.xz Raptor_Full_Output/">> postp.sbatch
echo "rm to_rm.list" >> postp.sbatch
echo "rm taskRaptor.list" >> postp.sbatch
echo "rm *.out" >> postp.sbatch
	
echo "#!/usr/bin/env bash" >> tango.sbatch
echo "#SBATCH --time=1:00:00" >> tango.sbatch
echo "#SBATCH --ntasks=1" >> tango.sbatch
echo "#SBATCH --nodes=1" >> tango.sbatch
echo "#SBATCH --cpus-per-task=1" >> tango.sbatch
echo "n=1;m=1;mkdir T;"  >> tango.sbatch
echo "echo -e "'"'"Sequence"'\'"tAggregation"'\'"tConc_Stab_Aggregation"'"'" >> tango_aggregation.txt" >> tango.sbatch
echo "for file in *.fasta" >> tango.sbatch
echo "do " >> tango.sbatch
echo "    echo "'"''$'"n N N 7.0 298 0.02 "'$'"(echo "'$'"seq "'|'" awk -F: 'NR==2 {print "'$'"1}' "'$'"{file})"'"'" >> T/tango.list" >> tango.sbatch
echo "    echo "'"''$'"{file"'%'".fasta} "'$'"n"'"'" >> T/tango_index.txt" >> tango.sbatch
echo "    echo "'"''$'"{file"'%'".fasta} "'$'"m"'"'" >> tango_index.txt" >> tango.sbatch
echo "    ${path_to_Tango} -inputfile=T/tango.list" >> tango.sbatch
echo "    if [ "'$'"m -eq 1 ]" >> tango.sbatch
echo "    then" >> tango.sbatch
echo "        mv 1.txt _1.txt" >> tango.sbatch
echo "    fi" >> tango.sbatch
echo "    if [ "'$'"m -gt 1 ]" >> tango.sbatch
echo "    then" >> tango.sbatch
echo "        mv 1.txt "'$'"m.txt" >> tango.sbatch
echo "    fi" >> tango.sbatch
echo "    mv -n T/tango_aggregation.* T/tango_aggregation.txt" >> tango.sbatch
echo "    t="'$'"(sed -n '2p' T/tango_aggregation.txt)" >> tango.sbatch
echo "    tm="'$'"(echo "'"''$'"t"'"'" | cut -d ' ' -f 2-)" >> tango.sbatch
echo "    echo -e "'"''$'"m"'\'"t"'$'"tm"'"'" >> tango_aggregation.txt" >> tango.sbatch
echo "    m="'$'"((m+1))" >> tango.sbatch
echo "    rm T/*" >> tango.sbatch
echo "done" >> tango.sbatch
echo "mv _1.txt 1.txt" >> tango.sbatch
echo "rm -r T" >> tango.sbatch

jobID1=$(sbatch --parsable rapt.sbatch)
jobID2=$(sbatch --dependency=afterok:${jobID1} --parsable postp.sbatch)
jobID3=$(sbatch --dependency=afterok:${jobID2} --parsable tango.sbatch)


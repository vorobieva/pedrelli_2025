#!/bin/bash

module load  Python/3.11.3-GCCcore-12.3.0

tar -xvf inside.tar
code=$(python preparation.py; echo $?)
module purge

cleaning () {
    rm -r __pycache__
    rm preparation.py
    rm plot.ipynb
    rm -r tmp
    rm params.py
}

if [[ $code == 1 ]]
then
    echo -------------
    echo Please fix params.txt to proper format. Example provided in README
    cleaning
    return 1
elif [[ $code == 2 ]]
then
    echo -------------
    echo PDB file does not present in the folder.
    echo -------------
    echo probably: The file names do not match.
    cleaning
    return 2
elif [[ $code == 3 ]]
then
    echo -------------
    echo File name parameter in params.txt is empty.
    cleaning
    return 3
elif [[ $code == 4 ]]
then
    echo -------------
    echo Provided name of XML file in params.txt is not in the folder.
    cleaning
    return 4
fi

cp params.py tmp/mutations/
cd tmp
jobID1=$(sbatch --parsable cmd.jobs)
jobID2=$(sbatch --dependency=afterok:${jobID1} --parsable scoring.jobs)
cd mutations
jobID3=$(sbatch --dependency=afterok:${jobID2} --parsable cmd_ddg.jobs)
jobID4=$(sbatch --dependency=afterok:${jobID3} --parsable analyze.jobs)

cd ../../

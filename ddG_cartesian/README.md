
Here it is one script for ΔΔG calculations.

This script allows to obtain ΔΔG values with almost one-line command.

At the end of all calculations evaluation the SSM_ddg.csv file will be generated.

The structure of CSV file is following:
    - columns are placed in ascending position order 
    - rows are placed NOT in alphabetical order; generated order:
        ["G","P","E","D","R","K","H","Q","N","T","S","Y","W","F","M","C","I","L","V","A"]

For final heatmap visualization the additionaly generated Jupyter notebook (plot.ipynb) could be used.
required packages for plot.ipynb are following: numpy, pandas, seaborn, matplotlib, plotly, ipywidgets, nbformat


Required files:
    1.  Your PDB file for one-point mutations estimation.
    2.  inside.tar
    3.  params.txt
    4.  run.sh
    5.  Optional: XML script for structure relaxation.

Usage:
    1. Copy all mentioned above files to your working directory.

    2. Edit "params.txt" file:
        Required
        2.1 pdb_name                - enter the full (with .pdb extension) file name;
        2.2 mut                     - enter list of investigated mutations in Python format;
        2.3 aa_list                 - list of tested mutations in each point provided in "mut" list
        2.4 path_to_Rosetta_main    - path to Rosetta software main folder. Ex: /some_space/Rosetta/main/

        Optional
        2.5 email                   - could be empty, or be filled in case of wish to obatin email notificitions when everything will be done;
        2.6 sbatch_array_length     - default: 100; recommended not to overcome 200 
        2.7 ntraj                   - default: 20; the amount of trajectories to structure relaxation before Î”Î”G calc;
        2.8 nstruct                 - default: 2; the value of relaxed structures from each trajectory;
        2.9 name_relax_xml          - could be empty, or be filled by the name of non-default XML script used for structure relaxation.
        2.10 ddg_iterations          - default: 3; 
        2.11 force_iterations        - default: False; if this flag is on the protocol will stop when the results converge on a score
        2.12 ddg_score_cutoff       - default: 1.0; if the lowest energy scores are within this cutoff the protocol will end early.
        2.13 ddg_dump_pdbs          - default: False; you can save mutants pdb if you want
        2.14 ddg_bbnbrs             - default: 1; bb dof, suggestion: i-1, i, i+1
        2.15 fa_max_dis             - default: 9.0;  modify fa_atr and fa_sol behavior, really important for protein stability
        2.16 score_weights          - default: ref2015_cart.wts 

    3. run "run.sh" by typing:
        . run.sh


Example of typical "params.txt":

pdb_name = 'Protein.pdb'
mut = ['M8', 'V12']
aa_list = ['A','C','D']
path_to_Rosetta_main = '/some_space/Rosetta/main/'

email = '' #could be filled in case of the notification receipt wish upon completion of calculations

#rosetta relax coords params
name_relax_xml = ''
ntraj = 20
nstruct = 2

#rosetta ddG calculations params
ddg_iterations = 3
force_iterations = False
ddg_score_cutoff = 1.0
ddg_dump_pdbs = False
ddg_bbnbrs = 1
fa_max_dis = 9.0
score_weights = 'ref2015_cart.wts'


import glob
import os
import pandas as pd
import numpy
from scipy.stats.stats import pearsonr
import sys

NAME = sys.argv[1]
structure = sys.argv[2]

def aa_distribution(sequence, dround, design_name):
    aa_dict = {"A": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0, "I": 0, "K": 0,
               "L": 0, "M": 0, "N": 0, "P": 0, "Q": 0, "R": 0, "S": 0, "T": 0, "V": 0, "W": 0, "Y": 0}
    n_resi = 0.0
    
    positions = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 35, 36, 37, 38, 39, 40, 41, 42, 43, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 65, 66,
                     67, 68, 69, 70, 71, 72, 73, 74, 75, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 97, 98, 99, 100, 101, 102, 103, 104, 105, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121]

    for pos in positions:
        aa_dict[sequence[pos-1]] = aa_dict[sequence[pos-1]] + 1
        n_resi += 1.0
    for key in aa_dict:
        aa_dict[key] = aa_dict[key]/n_resi
    return (aa_dict)


def aa_distribution_core(sequence, dround, design_name):
    aa_dict = {"A": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0, "I": 0, "K": 0,
               "L": 0, "M": 0, "N": 0, "P": 0, "Q": 0, "R": 0, "S": 0, "T": 0, "V": 0, "W": 0, "Y": 0}
    n_resi = 0.0
    
    positions = [6, 8, 10, 12, 14, 22, 24, 26, 28, 30, 36, 38, 40, 42, 50, 52, 54, 56, 58, 60,
                     66, 68, 70, 72, 74, 82, 84, 86, 88, 90, 92, 98, 100, 102, 104, 112, 114, 116, 118, 120]

    for pos in positions:
        aa_dict[sequence[pos-1]] = aa_dict[sequence[pos-1]] + 1
        n_resi += 1.0
    for key in aa_dict:
        aa_dict[key] = aa_dict[key]/n_resi

    return (aa_dict)


def aa_distribution_surface(sequence, dround, design_name):
    aa_dict = {"A": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0, "I": 0, "K": 0,
               "L": 0, "M": 0, "N": 0, "P": 0, "Q": 0, "R": 0, "S": 0, "T": 0, "V": 0, "W": 0, "Y": 0}
    n_resi = 0.0
    
    positions = [7, 9, 11, 13, 15, 21, 23, 25, 27, 29, 31, 35, 37, 39, 41, 43, 49, 51, 53, 55, 57, 59, 61,
                     65, 67, 69, 71, 73, 75, 81, 83, 85, 87, 89, 91, 93, 97, 99, 101, 103, 105, 111, 113, 115, 117, 119, 121]
    for pos in positions:
        aa_dict[sequence[pos-1]] = aa_dict[sequence[pos-1]] + 1
        n_resi += 1.0
    for key in aa_dict:
        aa_dict[key] = aa_dict[key]/n_resi

    return (aa_dict)


hydro_scale = {"A": 1.800, "C": 2.500, "D": -3.500, "E": -3.500, "F": 2.800, "G": -0.400, "H": -3.200, "I": 4.500, "K": -3.900, "L": 3.800,
               "M": 1.900, "N": -3.500, "P": -1.600, "Q": -3.500, "R": -4.500, "S": -0.800, "T": -0.700, "V": 4.200, "W": -0.900, "Y": -1.300}


def GRAVY(sequence):
    tot_score = 0
    for aa in sequence:
        tot_score += hydro_scale[aa]
    hydro_score = tot_score/len(sequence)

    return hydro_score


hydro_scale = {"A": 1.800, "C": 2.500, "D": -3.500, "E": -3.500, "F": 2.800, "G": -0.400, "H": -3.200, "I": 4.500, "K": -3.900, "L": 3.800,
               "M": 1.900, "N": -3.500, "P": -1.600, "Q": -3.500, "R": -4.500, "S": -0.800, "T": -0.700, "V": 4.200, "W": -0.900, "Y": -1.300}


def GRAVY_core(sequence, dround, design_name):
    tot_score = 0
    n_resi = 0.0
    
    positions = [6, 8, 10, 12, 14, 22, 24, 26, 28, 30, 36, 38, 40, 42, 50, 52, 54, 56, 58, 60,
                     66, 68, 70, 72, 74, 82, 84, 86, 88, 90, 92, 98, 100, 102, 104, 112, 114, 116, 118, 120]

    for pos in positions:
        tot_score += hydro_scale[sequence[pos-1]]
        n_resi += 1.0
    hydro_score = tot_score/n_resi

    return (hydro_score)


hydro_scale = {"A": 1.800, "C": 2.500, "D": -3.500, "E": -3.500, "F": 2.800, "G": -0.400, "H": -3.200, "I": 4.500, "K": -3.900, "L": 3.800,
               "M": 1.900, "N": -3.500, "P": -1.600, "Q": -3.500, "R": -4.500, "S": -0.800, "T": -0.700, "V": 4.200, "W": -0.900, "Y": -1.300}


def GRAVY_surf(sequence, dround, design_name):
    tot_score = 0
    n_resi = 0.0
    
    positions = [7, 9, 11, 13, 15, 21, 23, 25, 27, 29, 31, 35, 37, 39, 41, 43, 49, 51, 53, 55, 57, 59, 61,
                     65, 67, 69, 71, 73, 75, 81, 83, 85, 87, 89, 91, 93, 97, 99, 101, 103, 105, 111, 113, 115, 117, 119, 121]

    for pos in positions:
        tot_score += hydro_scale[sequence[pos-1]]
        n_resi += 1.0
    hydro_score = tot_score/n_resi

    return (hydro_score)


hydro_scale = {"A": 1.800, "C": 2.500, "D": -3.500, "E": -3.500, "F": 2.800, "G": -0.400, "H": -3.200, "I": 4.500, "K": -3.900, "L": 3.800,
               "M": 1.900, "N": -3.500, "P": -1.600, "Q": -3.500, "R": -4.500, "S": -0.800, "T": -0.700, "V": 4.200, "W": -0.900, "Y": -1.300}


def GRAVY_core_native(sequence, design, ref_ss):
    tot_score = 0
    n_resi = 0.0
    n = 0
    positions = []
    for i in range(0, len(ref_ss)):
        if ref_ss[i] == "E":
            n += 1
            if n % 2 == 0:
                positions.append(i+1)
            else:
                pass
        elif ref_ss[i] == "C":
            n = 0
    print(positions)
    for pos in positions:
        tot_score += hydro_scale[sequence[pos-1]]
        n_resi += 1.0
    hydro_score = tot_score/n_resi

    return (hydro_score)


hydro_scale = {"A": 1.800, "C": 2.500, "D": -3.500, "E": -3.500, "F": 2.800, "G": -0.400, "H": -3.200, "I": 4.500, "K": -3.900, "L": 3.800,
               "M": 1.900, "N": -3.500, "P": -1.600, "Q": -3.500, "R": -4.500, "S": -0.800, "T": -0.700, "V": 4.200, "W": -0.900, "Y": -1.300}


def GRAVY_surf_native(sequence, design, ref_ss):
    tot_score = 0
    n_resi = 0.0
    n = 0
    positions = []
    for i in range(0, len(ref_ss)):
        if ref_ss[i] == "E":
            n += 1
            if n % 2 != 0:
                positions.append(i+1)
            else:
                pass
        elif ref_ss[i] == "C":
            n = 0
    print(positions)
    for pos in positions:
        tot_score += hydro_scale[sequence[pos-1]]
        n_resi += 1.0
    hydro_score = tot_score/n_resi

    return (hydro_score)


def ss_pred(ss, dround, design_name):
    match = 0.0
    
    reference_ss = "CCCCCEEEEEEEEEEECCCEEEEEEEEEEEEECCEEEEEEEEEECCCEEEEEEEEEEEEEEECCEEEEEEEEEEEECCCEEEEEEEEEEEEEEECCEEEEEEEEEECCCEEEEEEEEEEEECC"

    for i in range(0, len(ss)):
        if reference_ss[i] == ss[i]:
            match += 1.0
    identity = match/len(ss)
    return identity


def ss_pred_native(ss, name, ref_ss):
    match = 0.0
    for i in range(0, len(ss)):
        if ref_ss[i] == ss[i]:
            match += 1.0
    identity = match/len(ss)
    return identity


pd.options.display.max_colwidth = 200
columns = ['sequence', 'ss', 'identity', 'hydropathy', 'hydropathy_core', 'hydropathy_surface',
           'ratio_hydropathy', 'F', 'aro', 'beta_sheet', 'coil', 'helix', "Aggregation propensity", 'result']
native = {'A': 0.09892494045990434, 'C': 0.0007037625203442372, 'D': 0.027770177581332288, 'E': 0.029719275383167428, 'F': 0.07929574855980195, 'G': 0.1453262552782189, 'H': 0.011157715202304692, 'I': 0.05289172587768166, 'K': 0.02000481398009908, 'L': 0.11207876498844926,
          'M': 0.01748405604149801, 'N': 0.02587373268683085, 'P': 0.026855803431653235, 'Q': 0.021940748555100798, 'R': 0.037856030027200865, 'S': 0.04138471504904712, 'T': 0.04080177214642398, 'V': 0.09253231337129984, 'W': 0.02589065683561668, 'Y': 0.09150699202402476}
native_core = {'A': 0.07307786630111489, 'C': 0.000560694380689476, 'D': 0.0529505100746824, 'E': 0.06357016644762904, 'F': 0.03465929694164796, 'G': 0.24388319111608575, 'H': 0.014590630220483895, 'I': 0.01795479650462075, 'K': 0.036906266571925035, 'L': 0.033595549658657645,
               'M': 0.022868994543972065, 'N': 0.04843456224965258, 'P': 0.010193109432870735, 'Q': 0.04258971634104471, 'R': 0.07494859428154613, 'S': 0.07878122858095064, 'T': 0.06227166114356501, 'V': 0.027519089809615437, 'W': 0.0037320237189443434, 'Y': 0.056912051680301494}
native_surf = {'A': 0.11995082543027749, 'C': 0.000820144522764552, 'D': 0.0072866686445619815, 'E': 0.0021825051749243796, 'F': 0.11560627606644364, 'G': 0.06515289471799646, 'H': 0.00836513311576485, 'I': 0.08131195842327642, 'K': 0.006255946474060585, 'L': 0.17592270521516432,
               'M': 0.013103556460385826, 'N': 0.007521117442649561, 'P': 0.040410447379459216, 'Q': 0.005143380359499524, 'R': 0.0076822477075170256, 'S': 0.010963678339659189, 'T': 0.02333660709109572, 'V': 0.14541878523126028, 'W': 0.0439160963166815, 'Y': 0.11964902588655747}


agg = pd.read_csv("tango_aggregation.txt", header=0, sep="\s+")
agg_index = pd.read_csv("tango_index.txt", header=None, names=[
                        "description", "Sequence"], sep="\s+")
daggregation = pd.merge(agg, agg_index, on="Sequence")
aggregation_list = daggregation[["Aggregation", "description"]].set_index(
    'description').to_dict()

df_res = pd.DataFrame(columns=columns)

for file in glob.glob("*.ss3_simp"):
    name = (file.split('/')[-1]).split('.')[0]
    sequence = ""
    ss = ""
    dround = NAME
    if name in aggregation_list["Aggregation"]:
        aggregation = aggregation_list["Aggregation"][name]
    else:
        aggregation = 50.0
    result = NAME

    with open(file, 'r') as in_f:
        lines = in_f.readlines()
        for i in range(0, len(lines)):
            line_seq = lines[1].strip()
            line_ss = lines[2].strip()

    sequence = line_seq.strip()
    ss = line_ss.strip()

    identity = ss_pred(ss, dround, name)
    distr = aa_distribution(sequence, dround, name)
    distr_surf = aa_distribution_surface(sequence, dround, name)
    distr_core = aa_distribution_core(sequence, dround, name)


    keys = set(native.keys()) | set(distr.keys())

    dstr_r = numpy.corrcoef([native.get(x, 0) for x in keys], [
                            distr.get(x, 0) for x in keys])[0, 1]
    dstr_core_r = numpy.corrcoef([native_core.get(x, 0) for x in keys], [
                                 distr_core.get(x, 0) for x in keys])[0, 1]
    dstr_surf_r = numpy.corrcoef([native_surf.get(x, 0) for x in keys], [
                                 distr_surf.get(x, 0) for x in keys])[0, 1]

    hydro = GRAVY(sequence)
    hydro_core = GRAVY_core(sequence, dround, name)
    hydro_surf = GRAVY_surf(sequence, dround, name)
    hydro_diff = hydro_surf-hydro_core

    F_freq = sequence.count('F')/len(ss)*100
    aro_freq = sequence.count('F')/len(ss)*100 + sequence.count('Y') / \
        len(ss)*100 + sequence.count('W')/len(ss)*100
    beta_sheet = float(ss.count('E'))/len(ss)*100
    coil = float(ss.count('C'))/len(ss)*100
    helix = float(ss.count('H'))/len(ss)*100
    df_res.loc[name] = [sequence, ss, identity, hydro, hydro_core, hydro_surf,
                         hydro_diff, F_freq, aro_freq, beta_sheet, coil, helix, aggregation, result]

df_res.to_pickle('../' + NAME + '_to_analyse_' + structure + '.pickle')


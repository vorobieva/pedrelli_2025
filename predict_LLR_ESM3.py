#
# Created by Tamas Lazar (VIB-VUB CSB, Brussels, Belgium) in 2025 - github.com/lazartomi
# Inspiration from Amelie Schreiber: https://huggingface.co/blog/AmelieSchreiber/mutation-scoring
# 
# This code performs an in silico site saturation mutagenesis and predicts the effect of mutations
# on protein fitness using the ESM3 large protein language model.
#
# Usage: Add the inputs as arguments (protein name and sequence), and it outputs the
# log likelihood ratios (LLR) for all possible mutations along the protein sequence in CSV format
#    Arg1: protein_name
#    Arg2: sequence


from huggingface_hub import whoami
user = whoami(token="hf_xxxxxxxxxx")
import sys
import torch
import torch.nn.functional as F
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from esm.models.esm3 import ESM3
from esm.pretrained import ESM3_sm_open_v0, ESM3_structure_encoder_v0
from esm.sdk.api import ESM3InferenceClient, ESMProtein, GenerationConfig

model: ESM3InferenceClient = ESM3.from_pretrained("esm3_sm_open_v1").to("cpu") # or "cuda"
from esm.utils.constants.esm3 import (
    SEQUENCE_MASK_TOKEN,
)
from esm.tokenization.sequence_tokenizer import EsmSequenceTokenizer
tokenizer = EsmSequenceTokenizer()

labels = ['L','A','G','V','S','E','R','T','I','D','P','K','Q',\
          'N','F','Y','M','H','W','C']

protein_name = "WT"
if len(sys.argv)>=2:
    protein_name = sys.argv[1]
prompt = "DQATSLRILNNGH"
if len(sys.argv)>=3:
    prompt = sys.argv[2]

enc_prompt = tokenizer.encode(prompt, return_tensors="pt")
input = enc_prompt.clone().detach().unsqueeze(0)

start_pos = 1
end_pos = enc_prompt.shape[1] - 2
heatmap = np.zeros((20, end_pos - start_pos + 1))

# Calculate LLRs for each position and amino acid
for position in range(start_pos, end_pos + 1):
    # Mask the target position
    masked_input_ids = enc_prompt.clone()
    masked_input_ids[0, position] = tokenizer.mask_token_id
    
    # Get logits for the masked token
    with torch.no_grad():
        logits = model(sequence_tokens=masked_input_ids).sequence_logits
        
    # Calculate log probabilities
    probabilities = F.softmax(logits[0, position], dim=0)
    log_probabilities = torch.log(probabilities)
    
    # Get the log probability of the wild-type residue
    wt_residue = enc_prompt[0, position].item()
    log_prob_wt = log_probabilities[wt_residue].item()
    
    # Calculate LLR for each variant
    for i, amino_acid in enumerate(labels):
        log_prob_mt = log_probabilities[tokenizer.convert_tokens_to_ids(amino_acid)].item()
        heatmap[i, position - start_pos] = log_prob_mt - log_prob_wt

df = pd.DataFrame(heatmap)
cols = np.arange(1,len(prompt)+1).tolist()
cols = (" ".join(str(c) for c in cols)).split()
df.columns = [m+n for m,n in zip(list(prompt),cols)]
df.index = labels
df.to_csv("heatmap_LLR_"+protein_name+"_"+"esm3_sm_open_v0.csv")


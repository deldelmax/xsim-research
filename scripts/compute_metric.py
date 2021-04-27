import csv
import os
import sys

sys.path.append('.')

from normal_transformers.analysis.similarities import compute_similarity_all_layers_google
from normal_transformers.util.util_common import pickle_load_from_file

model_names_or_dirs = [
    "xlm-roberta-large",
    "xlm-roberta-base",
    "bert-base-multilingual-cased",
    "bert-base-multilingual-uncased",
    "distilbert-base-multilingual-cased",
    "xlm-mlm-100-1280"
]

# Example runs:
# python scripts/compute_metric.py mBERT_uncased cka mean en-en_shuf

if __name__ == '__main__':
    model_name_or_dir = sys.argv[1]
    sim_name = sys.argv[2]
    sent_rep_type = sys.argv[3]
    lang_pair = sys.argv[4]

    assert model_name_or_dir in model_names_or_dirs
    assert sim_name in ["cca", "pwcca", "svcca", "cka"] or "svcca_" in sim_name
    assert sent_rep_type in ["mean", "cls"]

    src_lang, tgt_lang = lang_pair.split("-")

    exp_folder = "experiments"
    savedir_base = f"{exp_folder}/assets/multilingual"
    datadir = f"{exp_folder}/data"
    savedir = f"{savedir_base}/{model_name_or_dir}/sim_scores"
    os.makedirs(savedir, exist_ok=True)
    savefile_path = f"{savedir}/xnli6_{sim_name}_{sent_rep_type}_{lang_pair}.csv"
    loadfile_path_base = f"{savedir_base}/{model_name_or_dir}/xnli_encoded/multinli.train"

    print(f"{model_name_or_dir} {sent_rep_type} {sim_name} {lang_pair}")
    # if os.path.isfile(savefile_path):
    #     input(f"File {savefile_path} exists. Press Enter to continue or Ctr+C to exit.")

    # load encoded data
    data_encoded_src = pickle_load_from_file(f"{loadfile_path_base}_sentemb_{sent_rep_type}.{src_lang}.pkl",
                                             verbose=True)
    data_encoded_tgt = pickle_load_from_file(f"{loadfile_path_base}_sentemb_{sent_rep_type}.{tgt_lang}.pkl",
                                             verbose=True)

    # compute metric
    sim_scores = compute_similarity_all_layers_google(M1=data_encoded_src, M2=data_encoded_tgt, sim_name=sim_name)

    # save
    with open(savefile_path, 'w', newline='') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(sim_scores)
    print(f"Saved to {savefile_path}")

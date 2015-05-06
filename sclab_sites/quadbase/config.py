promoter_options = [("0", "No offset"), ("100", "100 bp"), ("500", "500 bp"), ("1000", "1 Kb"),
                    ("2000", "2 Kb"), ("5000", "5 Kb"), ("10000", "10 Kb")]

variable_stems = ("2-3", "2-5", "3-5")
quad_stem_options = [("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"),
                     ("2-3", "2 - 3"), ("2-5", "2 - 5"), ("3-5", "3 - 5")]
#make sure quad_stem_options and variable stems have synchronized entries

quad_loop_options = [("1", "1"), ("3", "3"), ("5", "5"), ("7", "7"),
                     ("10", "10"), ("12", "12"), ("15", "15"), ("17", "17")]

databases = [("hg19", "Homo Sapiens (hg19)"), ("hg18", "Homo Sapiens (hg18)"),
             ("mm9", "Mus musculus (mm9)"), ("mm10", "Mus musculus (mm10)")]

quad_strand_options = [("both", "Both"), ("+", "Plus (+)"), ("-", "Minus (-)")]
#both option is custom tailored according to quadfinder function

import os
import json

if __name__ == "__main__":
    gene_list_location = os.path.join(os.path.dirname(os.getcwd()), 'static/quadbase_files')
else:
    gene_list_location = os.path.join(os.getcwd(), 'static/quadbase_files')

gene_list_files = ['hg19', 'mm9']
gene_list_dict = {}
for list_file in gene_list_files:
    with open(os.path.join(gene_list_location, list_file)) as handle:
        gene_list_dict[list_file] = handle.read().splitlines()

assemblies_json = open(os.path.join(gene_list_location, 'assemblies.json'))
assemblies2_json = open(os.path.join(gene_list_location, 'assemblies2.json'))
assemblies_data = json.load(assemblies_json)
assemblies2_data = json.load(assemblies2_json)
assemblies_json.close()
assemblies2_json.close()



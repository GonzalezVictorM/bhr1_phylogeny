# bhr1_phylogeny
Analyze the phylogeny of the bhr1 gene

## mycocsm_organism_list.xlsm
Contains the instructions to get the list of mycocosm portals with published genomes.

## jgi-api-list-retriever.py
Retrieves a csv with all the files in this portals. It is necessary sorth through this csv to select the ones we are interested in using the R code. we should end up with one file per portal.

## package_installer.R
Installs all packages you will need from R.

## phylogeny-wrangling.R
Organizes the phylogeny based on the recovered tax_IDs from mycocosm.

## file-list-wrangling.R
Selects the files that have proteomes, specifically in the Filtered Best section of Mycocosm. It will also highlight portals with none of this files. This is most likely due to the API.

After running the previous codes, the selection must continue manually as it is important to evaluate a proper distribution of species across genera,family, and orders.

## Pending
The goals was to make a code to do a batch request for the files and then a batch download, but I am on a bit of a rush so I am doing it manually as I already had most ofd the proteomes.

## extract-files.py
Check for compressed files and extract them.

## clean-fasta-files.py
Cleans up the names of the file to only contain the portal name and the protein names. Alkso creates a log to check if it was done correctly.

## custom-fasta-cleaner.py
Cleans up the remaining fasta files.

## complete-pfam-accession.py
Before running this code, you need to download the Pfam-A.hmm file from the Hmmer server. I will try to automate this later. The code will extract the complete accession numbers with the decimals as it seems they are necessary for hmmfetch command. in my case I have a list of TF pfams from Todd´s paper on fungal TFs: Prevalence of transcription factors in ascomycete and basidiomycete fungi.

## fetch-tf-hmms.sh
Takes the TF pfam hmm models from the Pfam-A.hmm file downloaded from interpro.

## batch-hmmscan.sh
SLURM batch request to run hmmscan of the 37 TF families on all the proteomes.

## fetch-tf-proteomes.py
Using the domtblout files from the hmmscan of the 37 TF families, it keeps only proteins that match those descriptions.

## of-tfs-test.sh
Test run of orthofinder in a selected set of proteomes (only with TF domain containing proteins).

## of-tfs.sh and of-all.sh
Runs orthofinder on all 150 proteomes. Do not be like me and remember to clean the extremely long or short proteins from the proteomes beforehand. The next two codes do that.

## proteome-cleaner.R
Uses an uppper and lower length limit to get rid of potentially incorrect protein models. I used 50 <= length <= 10,000 since I am working with TFs which are mostly standard length. However, if you want to study a different set, you can use different limits. There is no need to clean the Tfs onlöy files as those have been ran through hmmscan/search.

## proteome-joiner.R
Joins all cleaned up proteomes.

## plot-phylogeny-tree.R
Plots the phylogeny tree using the described tree.
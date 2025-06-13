# Clear environment (optional—consider if you really need to remove everything)
rm(list = ls())

# Load libraries
library("tidyverse")

# Create output directory if missing
out_dir <- "portal_phylogeny"
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

# Call the list of all files retrieved from JGI with the python code
all_mycocosm_files <- read.csv("all_files_metadata.csv")
all_organisms <- unique(all_mycocosm_files$organism)

retrieved_organisms <- all_mycocosm_files %>%
  filter(file_name != "NO FILES FOUND") %>%
  .$organism %>%
  unique

missing_organisms <- all_mycocosm_files %>%
  filter(file_name == "NO FILES FOUND") %>%
  .$organism %>%
  unique

# Create a phylogeny data table
phylogeny_data <- all_mycocosm_files %>%
  select(organism, starts_with("ncbi")) %>%
  unique()

# Separate the portals that had no files
phylogeny_data_missing <- phylogeny_data %>%
  filter(organism %in% missing_organisms)

# Separate the portals with at least one file with taxon ID
phylogeny_data_complete <- phylogeny_data %>%
  filter(!is.na(ncbi_taxon_id)) %>%
  unique()

# Separate the portals with no taxon id
phylogeny_data_incomplete <- phylogeny_data %>%
  filter(!organism %in% c(missing_organisms, phylogeny_data_complete$organism)) %>%
  unique()

# Look for duplicate taxonomies
double_phylogeny_organisms <- phylogeny_data_complete %>% 
  group_by(organism) %>% 
  summarise(count = n()) %>%
  filter(count>1) %>%
  ungroup() %>%
  .$organism

double_phylogeny <- phylogeny_data_complete %>%
  filter(organism %in% double_phylogeny_organisms)

single_phylogeny <- phylogeny_data_complete %>%
  filter(!organism %in% double_phylogeny_organisms)

# Check that the sum of all organisms matches
c(unique(single_phylogeny$organism),
  unique(double_phylogeny$organism),
  unique(phylogeny_data_missing$organism),
  unique(phylogeny_data_incomplete$organism)) %>% unique() %>%
  length() == length(all_organisms)
  
# Write the csv
write.csv(phylogeny_data_missing, 
          file.path(out_dir, "missing_portals_phylopgeny.csv"),
          row.names = F)
write.csv(phylogeny_data_incomplete, 
          file.path(out_dir, "portals_incomplete_phylogeny.csv"),
          row.names = F)
write.csv(single_phylogeny, 
          file.path(out_dir, "portals_single_phylogeny.csv"),
          row.names = F)
write.csv(double_phylogeny, 
          file.path(out_dir, "portals_double_phylogeny.csv"),
          row.names = F)
# Clear environment (optional—consider if you really need to remove everything)
rm(list = ls())

# Load libraries
library("tidyverse")

# Create output directory if missing
out_dir <- "filtered_file_list"
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

# Start removing files
proteome_files <- all_mycocosm_files %>%
  unique() %>%
  filter(
    !grepl("deflines", file_name),
    !grepl("promoters", file_name),
    !grepl("gff", file_name),
    !grepl("tab", file_name),
    !grepl("txt", file_name),
    !grepl("/.bam", file_name),
    !grepl("fastq", file_name),
    !grepl("alleles", file_name),
    grepl("Filtered Models", portal_display_location),
    grepl("protein", jat_label),
    
  )

proteome_files$organism %>% unique%>% length

# check for strains with two files
file_count <- proteome_files %>%
  group_by(organism) %>%
  summarise(count = n()) %>%
  ungroup()

proteome_files <- proteome_files %>%
  left_join(file_count)

# Separate the dingle file portals
single_proteome_files <- proteome_files %>%
  filter(count == 1)

multi_proteome_files <- proteome_files %>%
  filter(count > 1)

no_proteome_files <- all_mycocosm_files %>%
  filter(!organism %in% unique(proteome_files$organism))


# Write the csv
write.csv(single_proteome_files, 
          file.path(out_dir, "single_proteome_files.csv"),
          row.names = F)
write.csv(multi_proteome_files, 
          file.path(out_dir, "multi_proteome_files.csv"),
          row.names = F)
write.csv(no_proteome_files, 
          file.path(out_dir, "no_proteome_files.csv"),
          row.names = F)
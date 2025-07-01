# Clear environment (optional—consider if you really need to remove everything)
rm(list = ls())

# Load libraries
library("tidyverse")
library("Biostrings")

# Define and validate paths
proteome_dir <- "proteome_files"
all_proteomes_dir <- file.path(proteome_dir, "renamed_files")
file_pattern <- "\\.fasta$"

# Define the upper and lower length limits
upper_length <- 10000
lower_length <- 50

# Ensure input directories exist
required_dirs <- c(proteome_dir, all_proteomes_dir)
lapply(required_dirs, function(d) if (!dir.exists(d)) stop("Directory not found: ", d))

# Create output directory if missing
out_dir <- file.path(proteome_dir, "clean_files")
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)

# List all the proteome files
proteome_files <- list.files(all_proteomes_dir, pattern = file_pattern, full.names = TRUE)

# Check if any files were found
if (length(proteome_files) == 0) {
  stop("No FASTA files found in ", all_proteomes_dir, ". Please check the directory and file_pattern.")
}

# Loop through the files and clean them
for (file_name in proteome_files) { # Corrected: use file_name in loop
  cat("Processing file:", basename(file_name), "\n") # Added more informative message
  
  sequences <- readAAStringSet(file_name) # Corrected: use file_name
  if (length(sequences) == 0) {
    warning("No sequences found in ", basename(file_name), ". Skipping this file.\n")
    next
  }
  
  # Keep only the sequences within the limit lengths
  output_sequences <- sequences[width(sequences) >= lower_length & width(sequences) <= upper_length]
  
  # Save the correct sequences
  output_file <- file.path(out_dir, basename(file_name))
  writeXStringSet(output_sequences, file = output_file, format = "fasta")
  
  cat("Successfully filtered", length(sequences), "sequences from", basename(file_name), "into", length(output_sequences), "sequences saved to", output_file, "\n")
}

cat("Filtering complete for all proteomes.\n")
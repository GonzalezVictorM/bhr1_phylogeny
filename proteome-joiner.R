# Clear environment (optional—consider if you really need to remove everything)
rm(list = ls())

# Load libraries
library("tidyverse")
library("Biostrings")

# Define and validate paths
proteome_dir <- "proteome_files"
all_proteomes_dir <- file.path(proteome_dir, "clean_files")
file_pattern <- "\\.fasta$"

# Ensure input directories exist
required_dirs <- c(proteome_dir, all_proteomes_dir)
lapply(required_dirs, function(d) if (!dir.exists(d)) stop("Directory not found: ", d))

# Create output directory if missing
out_dir <- file.path(proteome_dir, "allinone_renamed")
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
output_file <- file.path(out_dir,"combined_proteomes.fasta") # Output FASTA file
output_file <- file.path(out_dir,"sequence_length.csv") # Output FASTA file

# List all the proteome files
proteome_files <- file.path(all_proteomes_dir, list.files(all_proteomes_dir))

# Read and combine FASTA files
combined_sequences <- AAStringSet()  # Initialize empty AAStringSet for protein sequences
for (file in proteome_files) {
  tryCatch({
    # Read FASTA file
    sequences <- readAAStringSet(file)
    if (length(sequences) == 0) {
      warning("No sequences found in ", basename(file))
      next
    }
    
    # Append sequences to combined set
    combined_sequences <- c(combined_sequences, sequences)
    cat("Processed", basename(file), "with", length(sequences), "sequences.\n")
  }, error = function(e) {
    warning("Failed to process ", basename(file), ": ", e$message)
  })
} 

# Check and write output
if (length(combined_sequences) == 0) {
  stop("No sequences were successfully read from any FASTA files.")
}

# Write combined sequences to a single FASTA file
writeXStringSet(combined_sequences, file = output_file, format = "fasta")
cat("Successfully combined", length(combined_sequences), "sequences into", output_file, "\n")

# Create table of sequence names and lengths
sequence_table <- data.frame(
  Sequence_Name = names(combined_sequences),
  Length = width(combined_sequences),
  stringsAsFactors = FALSE
)

# Save table to CSV
write.csv(sequence_table, file = output_csv, row.names = FALSE)
cat("Successfully created table with", nrow(sequence_table), "sequences in", output_csv, "\n")

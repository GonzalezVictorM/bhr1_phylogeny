# Clear environment (optional—consider if you really need to remove everything)
rm(list = ls())

# -----------------------------
# Load necessary libraries
# -----------------------------
library(tidyverse)
library(ggtree)
library(treeio)
library(ape)

# -----------------------------
# Define input paths
# -----------------------------
phyl_dir <- "phylogeny_analysis"
pipeline_dir <-file.path(phyl_dir, "geneious")
tree_dir <- file.path(pipeline_dir, "fasttree_files")
#tree_dir <- file.path(pipeline_dir, "iqtree_files")
septin_file <- file.path(phyl_dir, "Septins.csv")
tree_file <- file.path(tree_dir, "OG0000195_clean_Myo2_mafft_80trim_puhti_fasttree.newick")
tax_file <- "proteome_list_orthofinder.csv"
tax_outgroup_file <- file.path(phyl_dir,"outgroup_phylogeny.csv")
output_tree <- file.path(tree_dir,"OG0000195_clean_Myo2_mafft_80trim_puhti_fasttree.pdf")

# Check if files exist
if (!file.exists(tree_file)) stop("Tree file not found: ", tree_file)
if (!file.exists(septin_file)) stop("Septin file not found: ", septin_file)
if (!file.exists(tax_file)) stop("Taxonomy file not found: ", tax_file)
if (!file.exists(tax_outgroup_file)) stop("Taxonomy file not found: ", tax_file)

# -----------------------------
# Read input data
# -----------------------------
# Read tree
tree <- read.tree(tree_file)
if (is.null(tree) || length(tree$tip.label) == 0) {
  stop("Failed to read tree or tree has no tips: ", tree_file)
}

# Read taxonomic metadata
tax_data <- read.csv(tax_file) %>%
  full_join(read.csv(tax_outgroup_file)) %>%
  select(portal, name, phylum:genus) %>%
  mutate(portal = as.character(portal))
  
cat("Loaded taxonomic data with", nrow(tax_data), "rows.\n")

# Read septin renaming map
char_septins <- read.csv(septin_file)
if (!all(c("protein_id", "new_id") %in% colnames(char_septins))) {
  stop("Septins.csv must contain 'protein_id' and 'new_id' columns.")
}
cat("Loaded septin data with", nrow(char_septins), "rows.\n")

# -----------------------------
# Rename tip labels using Septins.csv
# -----------------------------
# Create label map
label_map <- setNames(tree$tip.label, tree$tip.label)
matched_ids <- char_septins$protein_id %in% tree$tip.label
if (!any(matched_ids)) {
  warning("No protein IDs in Septins.csv match tree tip labels.")
} else {
  label_map[char_septins$protein_id[matched_ids]] <- char_septins$new_id[matched_ids]
}
tree$tip.label <- unname(label_map[tree$tip.label])
cat("Renamed", sum(matched_ids), "tip labels.\n")

# -----------------------------
# Annotate tree with taxonomic metadata
# -----------------------------
# Extract portal ID from tip labels (assumes format like 'PortalID-SomeGene')
tip_metadata <- data.frame(label = tree$tip.label) %>%
  mutate(portal = str_split_i(label, "-", 1)) %>%
  left_join(tax_data, by = "portal")

# Check for unmatched portals
unmatched <- tip_metadata$portal[!tip_metadata$portal %in% tax_data$portal]
if (length(unmatched) > 0) {
  warning("Some tip labels could not be matched to taxonomic data: ", paste(head(unmatched, 5), collapse = ", "))
}

# Create ggtree object
tree_gg <- ggtree(tree) %<+% tip_metadata

# -----------------------------
# Plot tree with node numbers for manual inspection
# -----------------------------
p_nodes <- tree_gg +
  geom_tippoint(aes(color = phylum), size = 2) +
  geom_tiplab(size = 2, hjust = -0.1) +
  geom_nodelab(aes(label = node), size = 2, nudge_x = 0.01, nudge_y = 0.5) +  # Display node numbers
  theme_tree2() +
  theme(legend.position = "right")
print(p_nodes)
ggsave("tree_with_node_numbers.pdf", plot = p_nodes, width = 20, height = 45)
cat("Plotted tree with node numbers in tree_with_node_numbers.pdf\n")

# -----------------------------
# Extract tree and metadata
# -----------------------------
# Use the original tree with updated tip labels
tree_phylo <- tree  # Changed from tree_gg@phylo
tip_metadata <- tree_gg$data %>% filter(isTip) %>% select(label, class) ### Modify here for class or phylum

# Custom descendant function
getDescendants <- function(tree, node) {
  descendants <- tree$edge[tree$edge[, 1] == node, 2]
  for (kid in descendants) {
    if (kid > length(tree$tip.label)) {  # Internal node
      descendants <- c(descendants, getDescendants(tree, kid))
    }
  }
  return(descendants)
}

# -----------------------------
# Find phylum-pure clades
# -----------------------------
clade_labels <- list()
n_tips <- length(tree_phylo$tip.label)
internal_nodes <- (n_tips + 1):max(tree_phylo$edge)

for (node in internal_nodes) {
  descendants <- getDescendants(tree_phylo, node)
  tip_desc <- descendants[descendants <= n_tips]
  if (length(tip_desc) < 2) next
  
  tip_labels <- tree_phylo$tip.label[tip_desc]
  phyla <- tip_metadata %>%
    filter(label %in% tip_labels) %>%
    pull(class) %>% ### Modify here for class or phylum
    unique()
  
  if (length(phyla) == 1 && !is.na(phyla)) {
    clade_labels[[length(clade_labels) + 1]] <- list(node = node, phylum = phyla)
  }
}

# -----------------------------
# Remove nested clades
# -----------------------------
filtered_clades <- list()
for (i in seq_along(clade_labels)) {
  current <- clade_labels[[i]]
  is_nested <- FALSE
  for (j in seq_along(clade_labels)) {
    if (i == j) next
    other <- clade_labels[[j]]
    if (current$phylum == other$phylum && current$node %in% getDescendants(tree_phylo, other$node)) {
      is_nested <- TRUE
      break
    }
  }
  if (!is_nested) {
    filtered_clades[[length(filtered_clades) + 1]] <- current
  }
}
cat("Found", length(filtered_clades), "non-nested phylum-pure clades.\n")

# -----------------------------
# Plot with clade labels
# -----------------------------
p <- tree_gg +
  geom_tippoint(aes(color = phylum), size = 1.5) +
  geom_tiplab(size = 1.5, hjust = -0.1) +
  #theme_tree2() +
  theme(legend.position = "right")

for (clade in filtered_clades) {
  p <- p + geom_cladelab(node = clade$node, label = clade$phylum, offset = 0.5)
}

print(p)
ggsave(output_tree, plot = p, width = 20, height = 50, limitsize = FALSE)
